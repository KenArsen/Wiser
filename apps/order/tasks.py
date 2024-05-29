import email
import imaplib
import logging
import re
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

            expired_orders = Order.objects.filter(
                expires__lt=timezone.now(), status="PENDING"
            )
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
                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/html":
                                body = part.get_payload(decode=True).decode()
                    else:
                        body = msg.get_payload(decode=True).decode()

                    if not body:
                        logging.warning("Empty letter")
                        mail.store(num, "+FLAGS", "\\Seen")
                        continue

                    soup = BeautifulSoup(body, "html.parser")

                    order_data = extract_order_data(soup=soup)
                    if order_data:
                        save_order(order_data)
                        mail.store(num, "+FLAGS", "\\Seen")
                        continue
                    else:
                        mail.store(num, "+FLAGS", "\\Seen")
                        continue

                except Exception as e:
                    logging.error(f"Error {e}")
                    mail.store(num, "+FLAGS", "\\Seen")
                    continue
            mail.logout()
        num_unread_messages = len(message_ids[0].split())
        return {"status": "success", "unread_messages": num_unread_messages}
    except Exception as e:
        logging.error(f"Error {e}")


def extract_order_data(soup):
    order_data = {}

    try:
        html_text = soup.find("div", class_="divBidLoad").text.strip()
        order_number_match = re.search(r"Order #(\d+)", html_text)
        order_data["order_number"] = (
            order_number_match.group(1) if order_number_match else None
        )

        pick_up_location = soup.find("div", class_="column1").strong.text.strip()
        pick_up_datetime = (
            soup.find("div", class_="column1")
            .contents[-1]
            .strip()
            .replace(" EST", "")
            .replace(" CEN", "")
        )

        delivery_location = soup.find("div", class_="column3").strong.text.strip()
        delivery_datetime = (
            soup.find("div", class_="column3")
            .contents[-1]
            .strip()
            .replace(" EST", "")
            .replace(" CEN", "")
        )

        order_data["pick_up_location"] = pick_up_location
        order_data["pick_up_date"] = pick_up_datetime
        order_data["delivery_location"] = delivery_location
        order_data["delivery_date"] = delivery_datetime

        order_data["stops"] = soup.find("span", class_="numberStopsIcon").text.strip()

        broker_data = soup.find_all("div", class_="column4")[0].find_all(
            "p", class_="dataColumn"
        )
        i = 0
        if broker_data[i].strong.text.strip() == "Broker:":
            order_data["broker"] = broker_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["broker"] = None
        if broker_data[i].strong.text.strip() == "Broker phone:":
            order_data["broker_phone"] = broker_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["broker_phone"] = None
        if broker_data[i].strong.text.strip() == "Email:":
            order_data["broker_email"] = (
                broker_data[i].text.strip().split(":")[-1].strip()
            )
            i += 1
        else:
            order_data["broker_email"] = None
        if broker_data[i].strong.text.strip() == "Posted:":
            order_data["posted"] = (
                broker_data[i]
                .contents[-1]
                .strip()
                .rstrip(":")
                .replace(" EST", "")
                .replace(" CEN", "")
            )
            i += 1
        else:
            order_data["posted"] = None
        if broker_data[i].strong.text.strip() == "Expires:":
            order_data["expires"] = (
                broker_data[i]
                .contents[-1]
                .strip()
                .rstrip(":")
                .replace(" EST", "")
                .replace(" CEN", "")
            )
            i += 1
        else:
            order_data["expires"] = None
        if broker_data[i].strong.text.strip() == "Dock Level:":
            order_data["dock_level"] = (
                broker_data[i].contents[-1].strip().rstrip(":").lower() == "yes"
            )
            i += 1
        else:
            order_data["dock_level"] = False
        if broker_data[i].strong.text.strip() == "Hazmat:":
            order_data["hazmat"] = (
                broker_data[i].contents[-1].strip().rstrip(":").lower() == "yes"
            )
            i += 1
        else:
            order_data["hazmat"] = False
        if broker_data[i].strong.text.strip() == "CSA/Fast Load:":
            order_data["fast_load"] = (
                broker_data[i].contents[-1].strip().rstrip(":").lower == "yes"
            )
            i += 1
        else:
            order_data["fast_load"] = False
        if broker_data[i].strong.text.strip() == "Notes:":
            order_data["notes"] = broker_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["notes"] = None

        transport_data = soup.find_all("div", class_="column5")[0].find_all(
            "p", class_="dataColumn"
        )
        i = 0
        if transport_data[i].strong.text.strip() == "Amount:":
            order_data["amount"] = transport_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["amount"] = None
        if transport_data[i].strong.text.strip() == "Load Type:":
            order_data["load_type"] = transport_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["load_type"] = None
        if transport_data[i].strong.text.strip() == "Vehicle required:":
            order_data["vehicle_required"] = (
                transport_data[i].contents[-1].strip().rstrip(":")
            )
            i += 1
        else:
            order_data["vehicle_required"] = None
        if transport_data[i].strong.text.strip() == "Pieces:":
            order_data["pieces"] = transport_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["pieces"] = None
        if transport_data[i].strong.text.strip() == "Weight:":
            order_data["weight"] = transport_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["weight"] = None
        if transport_data[i].strong.text.strip() == "Dimensions:":
            order_data["dimensions"] = (
                transport_data[i].contents[-1].strip().rstrip(":")
            )
            i += 1
        else:
            order_data["dimensions"] = None
        if transport_data[i].strong.text.strip() == "Stackable:":
            order_data["stackable"] = (
                transport_data[i].contents[-1].strip().rstrip(":").lower() == "yes"
            )
        else:
            order_data["stackable"] = False

        # Determine the date format
        date_format = (
            "%m/%d/%Y %H:%M"
            if len(pick_up_datetime.split()[0].split("/")[2]) == 4
            else "%m/%d/%y %H:%M"
        )

        order_data["pick_up_date"] = (
            timezone.make_aware(datetime.strptime(pick_up_datetime, date_format))
            + timedelta(hours=6)
            if pick_up_datetime
            else None
        )
        order_data["delivery_date"] = (
            timezone.make_aware(datetime.strptime(delivery_datetime, date_format))
            + timedelta(hours=6)
            if delivery_datetime
            else None
        )
        order_data["posted"] = (
            timezone.make_aware(datetime.strptime(order_data["posted"], date_format))
            + timedelta(hours=6)
            if order_data["posted"]
            else None
        )
        order_data["expires"] = (
            timezone.make_aware(datetime.strptime(order_data["expires"], date_format))
            + timedelta(hours=6)
            if order_data["expires"]
            else None
        )

        return order_data
    except ValueError as ve:
        raise ValidationError({"error": f"A value error has occurred: {ve}"})
    except TypeError as te:
        raise ValidationError({"error": f"A type error has occurred: {te}"})


@transaction.atomic
def save_order(order_data):
    if not order_data.get("order_number"):
        raise ValidationError({"error": "This order number cannot be empty."})

    order = Order(**order_data)
    order.full_clean()
    order.save()

    logging.info(f"{'#' * 10} Order {order.id} saved to the database")
    return order
