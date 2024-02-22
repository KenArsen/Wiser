from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
from smtplib import SMTPException, SMTPAuthenticationError
from apps.letter.models import Letter
import logging


@shared_task
def send_email(letter_id):
    try:
        logging.info(f'Sending email for letter {letter_id}')
        letter = Letter.objects.select_related('driver_id', 'order_id').get(pk=letter_id)
        letter.order_id.order_status = 'PENDING'
        letter.order_id.save()
        if letter.driver_id.email:
            subject = 'New comment added'
            message = 'A new comment has been added:\n\n'
            send_mail(subject=subject,
                      message=message,
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[letter.driver_id.email],
                      fail_silently=False,  # Raise exception on failure
                      html_message=letter.comment)
    except (SMTPAuthenticationError, SMTPException) as e:
        print(f'Ошибка при отправке почты: {e}')
    except Letter.DoesNotExist:
        print(f'Объект Letter с id={letter_id} не найден')
    except Exception as e:
        print(f'Общая ошибка: {e}')
