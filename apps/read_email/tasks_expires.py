from celery import shared_task
from django.utils import timezone

from .models import Order


@shared_task
def deactivate_expired_order(order_id):
    current_time = timezone.localtime(timezone.now())
    try:
        order = Order.objects.get(pk=order_id, is_active=True, this_posting_expires_est__lte=current_time)
        if order.user is None:
            print(f"Время действия заказа: {order.order_number} истекло в: {order.this_posting_expires_est}")
            order.delete()
            print(f"Заказ с номером {order.order_number} удален")
        else:
            print(f"Время действия заказа {order.order_number} истекло. Заказ перемещен в историю")
            order.is_active = False
            order.save()
    except Order.DoesNotExist:
        pass
