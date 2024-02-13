from celery import shared_task
import logging

from .models import Order


@shared_task
def deactivate_expired_order(order_id):
    logging.info(f'####### Время удаление {order_id} #######')
    try:
        order = Order.objects.filter(pk=order_id).first()
        if order:
            if order.user is None:
                logging.info(f"Время действия заказа: {order.id} истекло в: {order.this_posting_expires_est}")
                order.delete()
                logging.info(f"Заказ с номером {order_id} удален")
            else:
                logging.info(f"Время действия заказа {order.order_number} истекло. Заказ перемещен в историю")
                order.is_active = False
                order.save()
        else:
            logging.info(f'Order уже удален')
    except Exception as e:
        logging.error(f'Error in order: deactivate_expired_order {str(e)}')
        raise ValueError(f"Error in order deactivate_expired_order {str(e)}")