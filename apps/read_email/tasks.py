from celery import shared_task

from .parser_gmail import process_and_save_emails


@shared_task
def process_and_save_emails_task():
    return process_and_save_emails()


@shared_task()
def delete_expired_data():
    from datetime import datetime
    from apps.read_email.models import Order

    expired_data = Order.objects.filter(this_posting_expires_est__lt=datetime.now())
    expired_data.delete()