from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_mail_to_order(letter):
    email_body = render_to_string('send_email.html', {'letter': letter})
    email = EmailMultiAlternatives(
        subject='',
        body=strip_tags(email_body),
        from_email=settings.EMAIL_HOST_USER,
        to=['tan.me4nik@gmail.com']
    )
    email.attach_alternative(email_body, 'text/html')
    email.send()