from celery import shared_task
from .parser_gmail import process_and_save_emails


@shared_task
def process_and_save_emails_task():
    return process_and_save_emails()
