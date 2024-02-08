from celery import shared_task

from .models import Order


@shared_task
def deactivate_expired_order(order_id):
    print(f'####### Время удаление {order_id} #######')
    try:
        order = Order.objects.get(pk=order_id)
        if order.user is None:
            print(f"Время действия заказа: {order.id} истекло в: {order.this_posting_expires_est}")
            print(f"Заказ с номером {order.order_number} удален")
            order.delete()
        else:
            print(f"Время действия заказа {order.order_number} истекло. Заказ перемещен в историю")
            order.is_active = False
            order.save()
    except Order.DoesNotExist as e:
        print(f'Ошибка на order:{order_id} deactivate_expired_order {e}')
        raise ValueError(f"No found order")
