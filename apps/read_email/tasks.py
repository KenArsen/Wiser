from celery import shared_task
import logging
from django.db.models import Q
from .parser_gmail import process_and_save_emails
from django.utils import timezone
from apps.read_email.models import Order


@shared_task
def process_and_save_emails_task():
    return process_and_save_emails()


@shared_task()
def delete_expired_data():
    logging.info('Удаление начинался')
    active_orders = Order.objects.filter(Q(this_posting_expires_est__lt=timezone.now()), ~Q(user=None))
    if active_orders.exists():
        logging.info(f"Время действия {active_orders.count()} заказов истекло. Перемещаем в историю...")
        active_orders.update(is_active=False)
        logging.info("Заказы перемещены в историю")

    expired_orders = Order.objects.filter(this_posting_expires_est__lt=timezone.now(), user=None)
    if expired_orders.exists():
        logging.info(f"Время действия {expired_orders.count()} заказов истекло. Удаляем записи...")
        expired_orders.delete()
        logging.info("Заказы удалены")
    logging.info('Удаление закончился')
