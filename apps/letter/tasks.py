from smtplib import SMTPException, SMTPAuthenticationError

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Letter


@shared_task
def send_email(comment):
    try:
        send_mail(subject='Subject',
                  message='Message',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=['tan.me4nik@gmail.com'],
                  html_message=comment)
        print('Сообщение успешно отправлено')
    except SMTPAuthenticationError:
        print('Ошибка аутентификации SMTP. Проверьте настройки почты.')
    except SMTPException as e:
        print(f'Ошибка SMTP: {e}')
    except Exception as e:
        print(f'Общая ошибка при отправке почты: {e}')