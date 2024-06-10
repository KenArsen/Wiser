import email
import imaplib
import logging
import pytz
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from celery import shared_task
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.order.models import Order


@shared_task()
def delete_expired_data():
    try:
        with transaction.atomic():
            logging.info("##### Started deleting expired data. #####")

            expired_orders = Order.objects.filter(expires_date__lt=timezone.now(), status="PENDING")
            for order in expired_orders:
                order.move_to_history()

            logging.info("##### Deletion of expired data completed #####")
    except Exception as e:
        logging.error(f"An error occurred while deleting expired data: {e}")


@shared_task()
def process_and_save_emails_task():
    try:
        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
            mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            mail.select("inbox")

            status, message_ids = mail.search(None, "UNSEEN")

            for num in message_ids[0].split():
                try:
                    status, msg_data = mail.fetch(num, "(RFC822)")
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    body = _get_email_body(msg)

                    if body:
                        soup = BeautifulSoup(body, "html.parser")
                        order_data = extract_order_data(soup)
                        if order_data:
                            save_order(order_data)
                            mail.store(num, "+FLAGS", "\\Seen")
                            continue

                    mail.store(num, "+FLAGS", "\\Seen")
                except Exception as e:
                    logging.error(f"Error {e}")
                    mail.store(num, "+FLAGS", "\\Seen")
                    continue

            mail.logout()
        num_unread_messages = len(message_ids[0].split())
        return {"status": "success", "unread_messages": num_unread_messages}
    except Exception as e:
        logging.error(f"Error {e}")


def _get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()


def extract_order_data(soup):
    order_data = {}

    try:
        target_div = soup.select('div[class*=content]')
        div_text = target_div[0].get_text(separator='\n', strip=True)
        lines = div_text.split('\n')

        # Извлечение данных
        order_data["order_number"] = int(lines[0].split('#')[1].strip())
        order_data["pick_up_location"] = lines[2].strip()
        pick_up_datetime = lines[3].strip()
        order_data["delivery_location"] = lines[5].strip()
        delivery_datetime = lines[6].strip()
        order_data["stops"] = lines[7].strip()

        order_data["broker"] = _extract_data(lines, 'Broker:')
        order_data["broker_email"] = _extract_data(lines, 'Email:')
        order_data["broker_phone"] = _extract_data(lines, 'Broker Phone:')
        posted_datetime = _extract_data(lines, 'Posted:')
        expires_datetime = _extract_data(lines, 'Expires:')
        order_data["dock_level"] = _extract_data(lines, 'Dock Level:').lower() == 'yes'
        order_data["hazmat"] = _extract_data(lines, 'Hazmat:').lower() == 'yes'
        order_data["amount"] = float(_extract_data(lines, 'Posted Amount:').replace('$', '').replace(' USD', ''))
        order_data["fast_load"] = _extract_data(lines, 'CSA/Fast Load:').lower() == 'yes'
        order_data["notes"] = _extract_data(lines, 'Notes:')
        order_data["load_type"] = _extract_data(lines, 'Load Type:')
        order_data["vehicle_required"] = _extract_data(lines, 'Vehicle required:')
        order_data["pieces"] = int(_extract_data(lines, 'Pieces:'))
        order_data["weight"] = int(_extract_data(lines, 'Weight:').split(' ')[0].strip())
        order_data["dimensions"] = _extract_data(lines, 'Dimensions:')
        order_data["stackable"] = _extract_data(lines, 'Stackable:').lower() == 'yes'

        format_date = _determine_date_format(pick_up_datetime)

        order_data["pick_up_date"] = _parse_datetime_with_timezone(pick_up_datetime, format_date)
        order_data["delivery_date"] = _parse_datetime_with_timezone(delivery_datetime, format_date)
        order_data["posted_date"] = _parse_datetime_with_timezone(posted_datetime, format_date)
        order_data["expires_date"] = _parse_datetime_with_timezone(expires_datetime, format_date)

        return order_data
    except ValueError as ve:
        raise ValidationError({"error": f"A value error has occurred: {ve}"})
    except TypeError as te:
        raise ValidationError({"error": f"A type error has occurred: {te}"})


def _determine_date_format(date_str):
    if len(date_str.split()[0].split("/")[2]) == 4:
        return "%m/%d/%Y %H:%M"
    else:
        return "%m/%d/%y %H:%M"


def _extract_data(data, keyword):
    try:
        return data[data.index(keyword) + 1].strip()
    except ValueError:
        return None


def _parse_datetime_with_timezone(date_str, format_date):
    timezone_suffix = 'UTC'
    if " EST" in date_str:
        timezone_suffix = 'US/Eastern'
    elif " CEN" in date_str:
        timezone_suffix = 'US/Central'

    date_str = date_str.replace(" EST", "").replace(" CEN", "")
    try:
        return (pytz.timezone(timezone_suffix).localize(datetime.strptime(date_str, format_date))
                + timedelta(hours=6))
    except ValueError:
        return None


@transaction.atomic
def save_order(order_data):
    if not order_data.get("order_number"):
        raise ValidationError({"error": "This order number cannot be empty."})

    order = Order(**order_data)
    order.full_clean()
    order.save()

    logging.info(f"Order {order.id} saved to the database")
    return order
