import logging
from smtplib import SMTPAuthenticationError, SMTPException

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from apps.letter.models import Letter
from apps.order.models import Order


@shared_task
def send_email(data):
    try:
        logging.info(f"***** Sending email for letter {data['id']} *****")
        letter = Letter.objects.get(id=data["id"])
        order = Order.objects.get(id=data["order_id"])
        order.order_status = "AWAITING_BID"
        order.save()
        if order.email:
            subject = "New comment added"
            message = "A new comment has been added:\n\n"
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.email, "arsen.kenjegulov.bj@gmail.com", "yryskeldiaidarbekuulu@gmail.com"],
                fail_silently=False,
                html_message=letter.comment,
            )
            logging.info(f"***** Email to {order.email} sent successfully *****")
    except Letter.DoesNotExist or Order.DoesNotExist:
        logging.error(f"***** Unable to send email for letter {data['id']} *****")
    except (SMTPAuthenticationError, SMTPException) as e:
        print(f"Ошибка при отправке почты: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")
