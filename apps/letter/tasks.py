import logging
from smtplib import SMTPAuthenticationError, SMTPException

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import exceptions

from apps.letter.models import Letter
from apps.order.models import Order


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
                recipient_list=["arsen.kenjegulov.bj@gmail.com", "yryskeldiaidarbekuulu@gmail.com"],
                fail_silently=False,
                html_message=letter.comment,
            )
            logging.info(f"***** Email to {order.email} sent successfully *****")
    except Letter.DoesNotExist or Order.DoesNotExist:
        raise exceptions.ValidationError({"detail": "No such letter or order found"})
    except (SMTPAuthenticationError, SMTPException) as e:
        raise exceptions.ValidationError({"error", f"{e}"})
    except Exception as e:
        raise exceptions.ValidationError({"error": f"{e}"})
