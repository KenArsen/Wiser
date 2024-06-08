import logging
from smtplib import SMTPAuthenticationError, SMTPException

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

from apps.order.repositories.interfaces.letter import ILetterRepository
from apps.order.services.interfaces.letter import ISendLetterService


def send_email(data, order):
    try:
        order.status = "AWAITING_BID"
        order.save(update_fields=["status", "updated_at"])
        if order.broker_email:
            subject = "New comment added"
            message = "A new comment has been added:\n\n"
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.broker_email],
                fail_silently=False,
                html_message=data["comment"],
            )
            logging.info(f"***** Email to {order.broker_email} sent successfully *****")
        else:
            logging.warning(f"No email address found for order {order.id}")
    except (SMTPAuthenticationError, SMTPException) as e:
        raise ValidationError({"error": str(e)})
    except Exception as e:
        raise ValidationError({"error": str(e)})


class SendLetterService(ISendLetterService):
    def __init__(self, letter_repository: ILetterRepository):
        self._letter_repository = letter_repository

    def send_letter(self, data, user):
        order = data.get("order", None)

        if hasattr(order, "letter"):
            order.letter.delete()

        self._letter_repository.create(data)
        order.user = user
        order.save(update_fields=["user", "updated_at"])
        send_email(data, order)
