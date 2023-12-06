from celery import shared_task
from django.utils import timezone
from .models import Order


@shared_task
def deactivate_expired_order(order_id):
    try:
        order = Order.objects.get(pk=order_id, is_active=True)
        current_time = timezone.localtime(timezone.now())

        if order.this_posting_expires_est <= current_time:
            if order.user is None:
                print(f"Время действия заказа: {order.order_number} истекло в: {order.this_posting_expires_est}")
                Order.objects.filter(pk=order_id).delete()
                print(f"Заказ с номером {order.order_number} удален")
            else:
                print(f"Время действия заказа {order.order_number} истекло. Заказ перемещен в историю")
                Order.objects.filter(pk=order_id).update(is_active=False)
    except Order.DoesNotExist:
        pass

