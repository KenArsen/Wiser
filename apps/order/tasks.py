import datetime
import email
import imaplib
import logging
import re

from bs4 import BeautifulSoup
from celery import shared_task
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from wiser_load_board.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER

from .models import Order


@shared_task
def deactivate_expired_order(order_id):
    logging.info(f"####### Время удаление {order_id} #######")
    try:
        order = Order.objects.filter(pk=order_id, order_status="DEFAULT").first()
        if order:
            if order.user is None:
                logging.info(f"Время действия заказа: {order.id} истекло в: {order.this_posting_expires_est}")
                order.delete()
                logging.info(f"Заказ с номером {order_id} удален")
            else:
                logging.info(f"Время действия заказа {order.order_number} истекло. Заказ перемещен в историю")
                order.is_active = False
                order.save()
        else:
            logging.info(f"Order {order_id} уже удален")
    except Exception as e:
        logging.error(f"Error in order: deactivate_expired_order {str(e)}")
        raise ValueError(f"Error in order deactivate_expired_order {str(e)}")


@shared_task()
def delete_expired_data():
    try:
        with transaction.atomic():
            logging.info("##### Начато удаление просроченных данных. #####")

            expired_orders = Order.objects.filter(
                this_posting_expires_est__lt=timezone.now(), is_active=True, order_status="DEFAULT"
            )
            for order in expired_orders:
                order.move_to_history()

            logging.info("##### Удаление просроченных данных завершено #####")
    except Exception as e:
        logging.error(f"Произошла ошибка при удалении данных с истекшим сроком действия: {e}")


@shared_task
def process_and_save_emails_task():
    try:
        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
            mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
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
                        logging.warning("Пустое письмо")
                        mail.store(num, "+FLAGS", "\\Seen")
                        continue

                    soup = BeautifulSoup(body, "lxml")
                    br_tags = soup.find_all("br")
                    for br_tag in br_tags:
                        br_tag.replace_with("\n")
                    div = soup.find("div")
                    if div:
                        h = div.text.strip()
                    else:
                        logging.warning("Ошибка при обработке почты")
                        mail.store(num, "+FLAGS", "\\Seen")
                        continue

                    order_data = extract_order_data(h)
                    if order_data:
                        save_order(order_data)
                        mail.store(num, "+FLAGS", "\\Seen")
                    else:
                        logging.warning("Недостаточно данных для создания заказа")
                        mail.store(num, "+FLAGS", "\\Seen")

                except Exception as e:
                    logging.error(f"Ошибка {num}", e)
                    mail.store(num, "+FLAGS", "\\Seen")
                    continue

            mail.logout()

        num_unread_messages = len(message_ids[0].split())
        return {"status": "success", "unread_messages": num_unread_messages}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


def extract_order_data(html_text):
    order_data = {}

    # Извлечение данных из HTML текста с помощью регулярных выражений
    email_matches = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", html_text)
    order_data["from_whom"] = email_matches[1] if len(email_matches) > 1 else ""

    order_data["pick_up_at"] = (
        re.search(r"Pick-up at: (.*?)\n", html_text).group(1).strip()
        if re.search(r"Pick-up at: (.*?)\n", html_text)
        else None
    )

    order_data["pick_up_date_CEN"] = (
        re.search(r"Pick-up date \(CEN\): (.*?)\n", html_text).group(1).strip()
        if re.search(r"Pick-up date \(CEN\): (.*?)\n", html_text)
        else None
    )

    order_data["pick_up_date_EST"] = (
        re.search(r"Pick-up date \(EST\): (.*?)\n", html_text).group(1).strip()
        if re.search(r"Pick-up date \(EST\): (.*?)\n", html_text)
        else None
    )

    order_data["deliver_to"] = (
        re.search(r"Deliver to: (.*?)\n", html_text).group(1).strip()
        if re.search(r"Deliver to: (.*?)\n", html_text)
        else None
    )

    order_data["deliver_date_CEN"] = (
        re.search(r"Delivery date \(CEN\): (.*?)\n", html_text).group(1).strip()
        if re.search(r"Delivery date \(CEN\): (.*?)\n", html_text)
        else None
    )

    order_data["deliver_date_EST"] = (
        re.search(r"Delivery date \(EST\): (.*?)\n", html_text).group(1).strip()
        if re.search(r"Delivery date \(EST\): (.*?)\n", html_text)
        else None
    )

    order_data["notes"] = (
        re.search(r"Notes: (.*?)\n", html_text).group(1).strip() if re.search(r"Notes: (.*?)\n", html_text) else None
    )

    order_data["miles"] = (
        re.search(r"Miles: (.*?)\n", html_text).group(1).strip() if re.search(r"Miles: (.*?)\n", html_text) else None
    )

    order_data["pieces"] = (
        re.search(r"Pieces: (.*?)\n", html_text).group(1).strip() if re.search(r"Pieces: (.*?)\n", html_text) else None
    )

    order_data["weight"] = (
        re.search(r"Weight: (.*?)\n", html_text).group(1).strip() if re.search(r"Weight: (.*?)\n", html_text) else None
    )

    order_data["dims"] = (
        re.search(r"Dims: (.*?) in.\n", html_text).group(1).strip()
        if re.search(r"Dims: (.*?) in.\n", html_text)
        else None
    )

    order_data["stackable"] = (
        re.search(r"Stackable \? : (.*?)\n", html_text).group(1).strip()
        if re.search(r"Stackable \? : (.*?)\n", html_text)
        else None
    )

    order_data["hazardous"] = (
        re.search(r"Hazardous \? : (.*?)\n", html_text).group(1).strip()
        if re.search(r"Hazardous \? : (.*?)\n", html_text)
        else None
    )

    order_data["fast_load"] = (
        re.search(r"FAST Load \? : (.*?)\n", html_text).group(1).strip()
        if re.search(r"FAST Load \? : (.*?)\n", html_text)
        else None
    )

    order_data["dock_level"] = (
        re.search(r"Dock Level \? : (.*?)\n", html_text).group(1).strip()
        if re.search(r"Dock Level \? : (.*?)\n", html_text)
        else None
    )

    order_data["suggested_truck_size"] = (
        re.search(r"Suggested Truck Size : (.*?)\n", html_text).group(1).strip()
        if re.search(r"Suggested Truck Size : (.*?)\n", html_text)
        else None
    )

    order_data["this_posting_expires_cen"] = (
        re.search(r"This posting expires \(CEN\): (.*?)\n", html_text).group(1).strip()
        if re.search(r"This posting expires \(CEN\): (.*?)\n", html_text)
        else None
    )

    order_data["this_posting_expires_est"] = (
        re.search(r"This posting expires \(EST\): (.*?)\n", html_text).group(1).strip()
        if re.search(r"This posting expires \(EST\): (.*?)\n", html_text)
        else None
    )

    company_info_match = re.search(r"If you are interested in this load, please contact[:]*([\s\S]+?)\n", html_text)
    if company_info_match:
        company_info = company_info_match.group(1).strip()
        company_info_lines = company_info.split("\n")
        if len(company_info_lines) >= 4:
            order_data["company_name"] = company_info_lines[0].strip()
            order_data["company_address"] = company_info_lines[1].strip()
            order_data["company_location"] = company_info_lines[2].strip()
            order_data["company_phone"] = company_info_lines[3].strip()
    else:
        logging.warning("Информация о компании не найдена")

    order_data["load_posted_by"] = (
        re.search(r"Load posted by: (.*?)\n", html_text).group(1).strip()
        if re.search(r"Load posted by: (.*?)\n", html_text)
        else None
    )
    order_data["phone"] = (
        re.search(r"Phone: (.*?)\n", html_text).group(1).strip() if re.search(r"Phone: (.*?)\n", html_text) else None
    )
    order_data["fax"] = (
        re.search(r"Fax: (.*?)\n", html_text).group(1).strip() if re.search(r"Fax: (.*?)\n", html_text) else None
    )
    order_data["order_number"] = (
        re.search(r"Please reference our ORDER NUMBER : (.*?)\n", html_text).group(1).strip()
        if re.search(r"Please reference our ORDER NUMBER : (.*?)\n", html_text)
        else None
    )

    order_data["pick_up_date_CEN"] = (
        timezone.make_aware(datetime.datetime.strptime(order_data["pick_up_date_CEN"], "%m/%d/%Y %H:%M"))
        + datetime.timedelta(hours=6)
        if order_data["pick_up_date_CEN"]
        else None
    )

    order_data["pick_up_date_EST"] = (
        timezone.make_aware(datetime.datetime.strptime(order_data["pick_up_date_EST"], "%m/%d/%Y %H:%M"))
        + datetime.timedelta(hours=6)
        if order_data["pick_up_date_EST"]
        else None
    )

    order_data["deliver_date_CEN"] = (
        timezone.make_aware(datetime.datetime.strptime(order_data["deliver_date_CEN"], "%m/%d/%Y %H:%M"))
        + datetime.timedelta(hours=6)
        if order_data["deliver_date_CEN"]
        else None
    )

    order_data["deliver_date_EST"] = (
        timezone.make_aware(datetime.datetime.strptime(order_data["deliver_date_EST"], "%m/%d/%Y %H:%M"))
        + datetime.timedelta(hours=6)
        if order_data["deliver_date_EST"]
        else None
    )

    order_data["this_posting_expires_cen"] = (
        timezone.make_aware(datetime.datetime.strptime(order_data["this_posting_expires_cen"], "%m/%d/%Y %H:%M"))
        + datetime.timedelta(hours=6)
        if order_data["this_posting_expires_cen"]
        else None
    )

    order_data["this_posting_expires_est"] = (
        timezone.make_aware(datetime.datetime.strptime(order_data["this_posting_expires_est"], "%m/%d/%Y %H:%M"))
        + datetime.timedelta(hours=6)
        if order_data["this_posting_expires_est"]
        else None
    )

    return order_data


@transaction.atomic
def save_order(order_data):
    try:
        if not order_data.get("order_number"):
            raise ValidationError({"error": "This order number cannot be empty"})

        order = Order(**order_data)
        order.full_clean()
        order.save()
        logging.info(f"Заказ {order.id} сохранен в базу")

        eta_time = order.this_posting_expires_est + datetime.timedelta(seconds=3)
        logging.info(f"ORDER id : {order.id} - ETA TIME : {eta_time}")
        logging.info(f"ORDER id : {order.id} - LOCAL TIME : {timezone.localtime(timezone.now())}")

        transaction.on_commit(lambda: deactivate_expired_order.apply_async((order.id,), eta=eta_time))
        logging.info(f"Запуск задачи для Expires {order.id}")
        logging.info(f"{order.id}: Время удаления через {eta_time - timezone.localtime(timezone.now())}")
        return order
    except ValidationError as e:
        logging.error(e)
    except Exception as e:
        logging.error(f"Ошибка при сохранении заказа: {e}")
