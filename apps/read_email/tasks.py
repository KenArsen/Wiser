from .parser_gmail import process_and_save_emails
from celery import shared_task
from django.utils import timezone
from django.db import transaction
import logging
from .models import Order

logger = logging.getLogger(__name__)


@shared_task
def process_and_save_emails_task():
    return process_and_save_emails()


@shared_task()
def delete_expired_data():
    try:
        with transaction.atomic():
            logger.info('##### Начато удаление просроченных данных. #####')

            active_orders_expired = Order.objects.filter(
                this_posting_expires_est__lt=timezone.now(),
                user__isnull=False
            )
            if active_orders_expired.exists():
                logger.info(
                    f"Достигнуто время истечения для активных ордеров: {active_orders_expired.count()}. Переносимся в историю...")
                active_orders_expired.update(is_active=False)
                logger.info("Заказы перемещены в историю")

            expired_orders = Order.objects.filter(
                this_posting_expires_est__lt=timezone.now(),
                user__isnull=True
            )
            if expired_orders.exists():
                logger.info(
                    f"Достигнуто время истечения для ордеров с истекшим сроком действия {expired_orders.count()}. Удаление записей...")
                expired_orders.delete()
                logger.info("Заказы удалены")

            logger.info('##### Удаление просроченных данных завершено #####')
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении данных с истекшим сроком действия: {e}")
