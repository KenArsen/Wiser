# from celery import shared_task
# from .parser import process_email
#
#
# @shared_task
# def read_gmail_task_v2():
#     from apps.read_email.parser import read_gmail
#     num_unread_messages = read_gmail()
#     return f"Найдено {num_unread_messages} непрочитанных сообщений"
#
#
# @shared_task
# def process_email_task_v2(email_data):
#     return process_email(email_data)
#


from celery import shared_task
from .parser_gmail import process_and_save_emails


@shared_task
def process_and_save_emails_task():
    return process_and_save_emails()
