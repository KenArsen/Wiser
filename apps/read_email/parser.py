import logging
import re
from bs4 import BeautifulSoup
import datetime
import imaplib
import email
import os
from wiser_load_board.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from wiser_load_board.celery import app
from apps.read_email.models import Order


@app.task
def process_email(email_data, file_path):
    body = email_data['body']

    if not body:
        print("Пустое body")
        return {"status": "Пустое письмо"}

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
            print(body)
            return {"status": "Ошибка при обработке почты"}

        from_filed = soup.find('a').text.strip()
        pickup_location = re.search(r'Pick-up at: (.*?)\n', h).group(1)

        pickup_date_cen_match = re.search(r'Pick-up date \(CEN\): (.*?)\n', h)
        pickup_date_cen = pickup_date_cen_match.group(1) if pickup_date_cen_match else None

        pickup_date_est_match = re.search(r'Pick-up date \(EST\): (.*?)\n', h)
        pickup_date_est = pickup_date_est_match.group(1) if pickup_date_est_match else None

        delivery_location = re.search(r'Deliver to: (.*?)\n', h).group(1)

        delivery_date_cen_match = re.search(r'Delivery date \(CEN\): (.*?)\n', h)
        delivery_date_cen = delivery_date_cen_match.group(1) if delivery_date_cen_match else None

        delivery_date_est_match = re.search(r'Delivery date \(EST\): (.*?)\n', h)
        delivery_date_est = delivery_date_est_match.group(1) if delivery_date_est_match else None

        notes = re.search(r'Notes: (.*?)\n', h).group(1)
        miles = re.search(r'Miles: (.*?)\n', h).group(1)
        pieces = re.search(r'Pieces: (.*?)\n', h).group(1)
        weight = re.search(r'Weight: (.*?)\n', h).group(1)

        dims_match = re.search(r'Dims: (.*?) in.\n', h)
        dims = dims_match.group(1) if dims_match else None

        stackable_match = re.search(r'Stackable \? : (.*?)\n', h)
        stackable = stackable_match.group(1) if stackable_match else None

        hazardous_match = re.search(r'Hazardous \? : (.*?)\n', h)
        hazardous = hazardous_match.group(1) if hazardous_match else None

        fast_load = re.search(r'FAST Load \? : (.*?)\n', h).group(1)
        dock_level = re.search(r'Dock Level \? : (.*?)\n', h).group(1)
        truck_size = re.search(r'Suggested Truck Size : (.*?)\n', h).group(1)

        this_posting_expires_cen_match = re.search(r'This posting expires \(CEN\): (.*?)\n', h)
        this_posting_expires_cen = this_posting_expires_cen_match.group(1) if this_posting_expires_cen_match else None

        this_posting_expires_est_match = re.search(r'This posting expires \(EST\): (.*?)\n', h)
        this_posting_expires_est = this_posting_expires_est_match.group(1) if this_posting_expires_est_match else None

        load_posted_by = re.search(r'Load posted by: (.*?)\n', h).group(1)
        phone = re.search(r'Phone: (.*?)\n', h).group(1)
        fax = re.search(r'Fax: (.*?)\n', h).group(1)
        order_number = re.search(r'Please reference our ORDER NUMBER : (.*?)\n', h).group(1)

        # Форматирование дат
        formatted_pickup_cen = datetime.datetime.strptime(pickup_date_cen, "%m/%d/%Y %H:%M") if pickup_date_cen else None
        formatted_pickup_est = datetime.datetime.strptime(pickup_date_est, "%m/%d/%Y %H:%M") if pickup_date_est else None
        formatted_deliver_cen = datetime.datetime.strptime(delivery_date_cen, "%m/%d/%Y %H:%M") if delivery_date_cen else None
        formatted_deliver_est = datetime.datetime.strptime(delivery_date_est, "%m/%d/%Y %H:%M") if delivery_date_est else None
        formatted_posting_cen = datetime.datetime.strptime(this_posting_expires_cen, "%m/%d/%Y %H:%M") if this_posting_expires_cen else None
        formatted_posting_est = datetime.datetime.strptime(this_posting_expires_est, "%m/%d/%Y %H:%M") if this_posting_expires_est else None

        try:
            print(Order.objects.get(order_number=order_number).order_number)
        except Order.DoesNotExist:
            print("Этот заказ не существует в бд")

        if Order.objects.filter(order_number=order_number).exists():
            print("Order с таким номером уже существует!")
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
        return {"status": "success"}
    except Exception as e:
        return {"status": "Ошибка при записи в бд"}


@app.task
def read_gmail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    mail.select('inbox')

    save_dir = 'email_html'
    os.makedirs(save_dir, exist_ok=True)

    status, message_ids = mail.search(None, 'UNSEEN')

    print(message_ids)

    for num in message_ids[0].split():
        print(num)
        status, msg_data = mail.fetch(num, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True).decode()
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        filename = f'{current_datetime}.html'
        file_path = os.path.join(save_dir, filename)
        with open(os.path.join(save_dir, filename), 'w') as html_file:
            html_file.write(body)

        mail.store(num, '+FLAGS', '\\Seen')

        email_data = {
            'body': body,
        }
        process_email_task.apply_async(kwargs={"email_data": email_data, "file_path": file_path})

    mail.logout()
    num_unread_messages = len(message_ids[0].split())
    return num_unread_messages


@app.task
def process_email_task(email_data, file_path):
    try:
        process_email(email_data, file_path)
        try:
            os.remove(file_path)
            logging.info(f"Удален файл: {file_path}")
        except Exception as e:
            logging.error(f"Ошибка при удалении файла: {file_path}, {str(e)}")
    except Exception as e:
        logging.error(f"Ошибка при обработке email: {str(e)}")
        return {"status": "Ошибка при записи в бд"}

