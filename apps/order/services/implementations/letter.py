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
            logging.info(f"Email sent successfully to {order.broker_email}")
        else:
            logging.warning(f"No email address found for order {order.id}")
    except SMTPAuthenticationError as e:
        logging.error(f"SMTP authentication failed: {str(e)}")
        raise ValidationError({"error": "SMTP authentication failed"})
    except SMTPException as e:
        logging.error(f"SMTP exception occurred: {str(e)}")
        raise ValidationError({"error": "Failed to send email"})
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise ValidationError({"error": "Unexpected error occurred"})


class SendLetterService(ISendLetterService):
    def __init__(self, repository: ILetterRepository):
        self._repository = repository

    def send_letter(self, data, user):
        order = data.get("order")

        if hasattr(order, "letter"):
            order.letter.delete()

        self._repository.create_letter(data)
        order.user = user
        order.save(update_fields=["user", "updated_at"])

        send_email(data, order)
