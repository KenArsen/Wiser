import email
import imaplib
import logging
import re
from datetime import datetime, timedelta

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
                logging.info(f"Время действия заказа: {order.id} истекло в: {order.expires}")
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

            expired_orders = Order.objects.filter(expires__lt=timezone.now(), is_active=True, order_status="DEFAULT")
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

                    soup = BeautifulSoup(body, "html.parser")

                    order_data = extract_order_data(soup=soup)
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


def extract_order_data(soup):
    order_data = {}

    try:
        html_text = soup.find("div", class_="divBidLoad").text.strip()
        order_number_match = re.search(r"Order #(\d+)", html_text)
        order_data["order_number"] = order_number_match.group(1) if order_number_match else None

        if soup.find("div", class_="column1").find("a"):
            pick_up_at = soup.find("div", class_="column1").a.strong.text.strip()
        else:
            pick_up_at = soup.find("div", class_="column1").strong.text.strip()
        pick_up_date = soup.find("div", class_="column1").contents[-1].strip().replace(" EST", "").replace(" CEN", "")

        if soup.find("div", class_="column3").find("a"):
            deliver_to = soup.find("div", class_="column3").a.strong.text.strip()
        else:
            deliver_to = soup.find("div", class_="column3").strong.text.strip()
        deliver_date = soup.find("div", class_="column3").contents[-1].strip().replace(" EST", "").replace(" CEN", "")

        order_data["line"] = soup.find("div", class_="line").text.strip()

        broker_data = soup.find_all("div", class_="column4")[0].find_all("p", class_="dataColumn")
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
            order_data["email"] = broker_data[i].text.strip().split(":")[-1].strip()
            i += 1
        else:
            order_data["email"] = None
        if broker_data[i].strong.text.strip() == "Posted:":
            order_data["posted"] = (
                broker_data[i].contents[-1].strip().rstrip(":").replace(" EST", "").replace(" CEN", "")
            )
            i += 1
        else:
            order_data["posted"] = None
        if broker_data[i].strong.text.strip() == "Expires:":
            order_data["expires"] = (
                broker_data[i].contents[-1].strip().rstrip(":").replace(" EST", "").replace(" CEN", "")
            )
            i += 1
        else:
            order_data["expires"] = None
        if broker_data[i].strong.text.strip() == "Dock Level:":
            order_data["dock_level"] = broker_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["dock_level"] = None
        if broker_data[i].strong.text.strip() == "Hazmat:":
            order_data["hazmat"] = broker_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["hazmat"] = None
        if broker_data[i].strong.text.strip() == "CSA/Fast Load:":
            order_data["fast_load"] = broker_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["fast_load"] = None
        if broker_data[i].strong.text.strip() == "Notes:":
            order_data["notes"] = broker_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["notes"] = None

        transport_data = soup.find_all("div", class_="column5")[0].find_all("p", class_="dataColumn")
        i = 0
        if transport_data[i].strong.text.strip() == "Load Type:":
            order_data["load_type"] = transport_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["load_type"] = None
        if transport_data[i].strong.text.strip() == "Vehicle required:":
            order_data["vehicle_required"] = transport_data[i].contents[-1].strip().rstrip(":")
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
            order_data["dimensions"] = transport_data[i].contents[-1].strip().rstrip(":")
            i += 1
        else:
            order_data["dimensions"] = None
        if transport_data[i].strong.text.strip() == "Stackable:":
            order_data["stackable"] = transport_data[i].contents[-1].strip().rstrip(":")
        else:
            order_data["stackable"] = None

        # Определение формата даты и времени
        date_format = "%m/%d/%Y %H:%M" if len(pick_up_date.split()[0].split("/")[2]) == 4 else "%m/%d/%y %H:%M"

        order_data["pick_up_at"] = pick_up_at
        order_data["pick_up_date"] = (
            timezone.make_aware(datetime.strptime(pick_up_date, date_format)) + timedelta(hours=6)
            if pick_up_date
            else None
        )
        order_data["deliver_to"] = deliver_to
        order_data["deliver_date"] = (
            timezone.make_aware(datetime.strptime(deliver_date, date_format)) + timedelta(hours=6)
            if deliver_date
            else None
        )

        order_data["posted"] = (
            timezone.make_aware(datetime.strptime(order_data["posted"], date_format)) + timedelta(hours=6)
            if order_data["posted"]
            else None
        )
        order_data["expires"] = (
            timezone.make_aware(datetime.strptime(order_data["expires"], date_format)) + timedelta(hours=6)
            if order_data["expires"]
            else None
        )

        return order_data
    except ValueError as ve:
        logging.error(f"Произошла ошибка значения: {ve}")
    except TypeError as te:
        logging.error(f"Произошла ошибка типа: {te}")


@transaction.atomic
def save_order(order_data):
    try:
        if not order_data.get("order_number"):
            raise ValidationError({"error": "Этот номер заказа не может быть пустым."})

        order = Order(**order_data)
        order.full_clean()
        order.save()
        logging.info(f"Заказ {order.id} сохранен в базу")

        eta_time = order.expires + timedelta(seconds=3)
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
