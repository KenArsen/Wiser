import re
import datetime
from django.utils import timezone
import imaplib
import email
from bs4 import BeautifulSoup
from wiser_load_board.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from .models import Order
from celery import shared_task
from .tasks_expires import deactivate_expired_order


@shared_task
def process_and_save_emails():
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        mail.select('inbox')

        status, message_ids = mail.search(None, 'UNSEEN')

        for num in message_ids[0].split():
            status, msg_data = mail.fetch(num, '(RFC822)')
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
                print("Пустое письмо")
                continue

            try:
                soup = BeautifulSoup(body, "lxml")
                br_tags = soup.find_all('br')
                for br_tag in br_tags:
                    br_tag.replace_with('\n')
                div = soup.find('div')
                if div:
                    h = div.text.strip()
                else:
                    print("Ошибка при обработке почты")
                    continue

                from_filed = soup.find('a').text.strip()

                pickup_location_match = re.search(r'Pick-up at: (.*?)\n', h)
                pickup_location = pickup_location_match.group(1) if pickup_location_match else None

                pickup_date_cen_match = re.search(r'Pick-up date \(CEN\): (.*?)\n', h)
                pickup_date_cen = pickup_date_cen_match.group(1) if pickup_date_cen_match else None

                pickup_date_est_match = re.search(r'Pick-up date \(EST\): (.*?)\n', h)
                pickup_date_est = pickup_date_est_match.group(1) if pickup_date_est_match else None

                delivery_location_match = re.search(r'Deliver to: (.*?)\n', h)
                delivery_location = delivery_location_match.group(1) if delivery_location_match else None

                delivery_date_cen_match = re.search(r'Delivery date \(CEN\): (.*?)\n', h)
                delivery_date_cen = delivery_date_cen_match.group(1) if delivery_date_cen_match else None

                delivery_date_est_match = re.search(r'Delivery date \(EST\): (.*?)\n', h)
                delivery_date_est = delivery_date_est_match.group(1) if delivery_date_est_match else None

                notes_match = re.search(r'Notes: (.*?)\n', h)
                notes = notes_match.group(1) if notes_match else None

                miles_match = re.search(r'Miles: (.*?)\n', h)
                miles = miles_match.group(1) if miles_match else None

                pieces_match = re.search(r'Pieces: (.*?)\n', h)
                pieces = pieces_match.group(1) if pieces_match else None

                weight_match = re.search(r'Weight: (.*?)\n', h)
                weight = weight_match.group(1) if weight_match else None

                dims_match = re.search(r'Dims: (.*?) in.\n', h) or re.search(r'Dims: (.*?)in.\n', h)
                dims = dims_match.group(1) if dims_match else None

                stackable_match = re.search(r'Stackable \? : (.*?)\n', h) or re.search(r'Stackable: (.*?)\n', h)
                stackable = stackable_match.group(1) if stackable_match else None

                hazardous_match = re.search(r'Hazardous \? : (.*?)\n', h) or re.search(r'Hazardous: (.*?)\n', h)
                hazardous = hazardous_match.group(1) if hazardous_match else None

                fast_load_match = re.search(r'FAST Load \? : (.*?)\n', h) or re.search(r'FAST load: (.*?)\n', h)
                fast_load = fast_load_match.group(1) if fast_load_match else None

                dock_level_match = re.search(r'Dock Level \? : (.*?)\n', h) or re.search(r'Dock Level: (.*?)\n', h)
                dock_level = dock_level_match.group(1) if dock_level_match else None

                truck_size_match = re.search(r'Suggested Truck Size : (.*?)\n', h) or re.search(r'Suggested Truck Size: (.*?)\n', h)
                truck_size = truck_size_match.group(1) if truck_size_match else None

                this_posting_expires_cen_match = re.search(r'This posting expires \(CEN\): (.*?)\n', h)
                this_posting_expires_cen = this_posting_expires_cen_match.group(
                    1) if this_posting_expires_cen_match else None

                this_posting_expires_est_match = re.search(r'This posting expires \(EST\): (.*?)\n', h)
                this_posting_expires_est = this_posting_expires_est_match.group(
                    1) if this_posting_expires_est_match else None

                load_posted_by_match = re.search(r'Load posted by: (.*?)\n', h)
                load_posted_by = load_posted_by_match.group(1) if load_posted_by_match else None

                phone_match = re.search(r'Phone: (.*?)\n', h)
                phone = phone_match.group(1) if phone_match else None

                fax_match = re.search(r'Fax: (.*?)\n', h)
                fax = fax_match.group(1) if fax_match else None

                order_number_match = (re.search(r'Please reference our ORDER NUMBER : (.*?)\n', h)
                                      or re.search(r'Please reference our ORDER NUMBER: (.*?)\n', h))
                order_number = order_number_match.group(1) if order_number_match else None

                # Форматирование дат
                formatted_pickup_cen = timezone.make_aware(
                    datetime.datetime.strptime(pickup_date_cen, "%m/%d/%Y %H:%M")) if pickup_date_cen else None
                formatted_pickup_est = timezone.make_aware(
                    datetime.datetime.strptime(pickup_date_est, "%m/%d/%Y %H:%M")) if pickup_date_est else None
                formatted_deliver_cen = timezone.make_aware(
                    datetime.datetime.strptime(delivery_date_cen, "%m/%d/%Y %H:%M")) if delivery_date_cen else None
                formatted_deliver_est = timezone.make_aware(
                    datetime.datetime.strptime(delivery_date_est, "%m/%d/%Y %H:%M")) if delivery_date_est else None
                formatted_posting_cen = timezone.make_aware(datetime.datetime.strptime(this_posting_expires_cen,
                                                                                       "%m/%d/%Y %H:%M")) if this_posting_expires_cen else None
                formatted_posting_est = timezone.make_aware(datetime.datetime.strptime(this_posting_expires_est,
                                                                                       "%m/%d/%Y %H:%M")) if this_posting_expires_est else None

                try:
                    print(Order.objects.get(order_number=order_number).order_number)
                except Order.DoesNotExist:
                    print(f"Заказ {order_number} сохранен в базу")

                if Order.objects.filter(order_number=order_number).exists():
                    print(f"Order номером {order_number} уже существует!")

                else:
                    order = Order(
                        from_whom=from_filed,
                        pick_up_at=pickup_location,
                        pick_up_date_CEN=formatted_pickup_cen,
                        pick_up_date_EST=formatted_pickup_est,
                        deliver_to=delivery_location,
                        deliver_date_CEN=formatted_deliver_cen,
                        deliver_date_EST=formatted_deliver_est,
                        notes=notes,
                        miles=miles,
                        pieces=pieces,
                        weight=weight,
                        dims=dims,
                        stackable=stackable,
                        hazardous=hazardous,
                        fast_load=fast_load,
                        dock_level=dock_level,
                        suggested_truck_size=truck_size,
                        this_posting_expires_cen=formatted_posting_cen,
                        this_posting_expires_est=formatted_posting_est,
                        load_posted_by=load_posted_by,
                        phone=phone,
                        fax=fax,
                        order_number=order_number,
                    )
                    order.save()

                    if order.this_posting_expires_est:
                        eta_time = order.this_posting_expires_est
                        deactivate_expired_order.apply_async((order.id,), eta=eta_time)
                        print(f"Запуск задачи для Expires {order.order_number}")

                mail.store(num, '+FLAGS', '\\Seen')

            except Exception as e:
                print(f"Ошибка {num}", e)
                continue

        mail.logout()

        num_unread_messages = len(message_ids[0].split())
        return {"status": "success", "unread_messages": num_unread_messages}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
