from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.common.enums import SubStatus
from .order_service import OrderService


class MyLoadService(OrderService):

    def _get_order(self, data):
        order_id = data.get("order")
        if order_id is None:
            raise ValidationError({"detail": "order field is required."})
        order = self.get_order(pk=order_id)
        return order

    def _update_status(self, order, current_status):
        next_status = current_status + 1
        previous_status = current_status - 1 if current_status > SubStatus.POINT_A else None

        order.my_load_status.previous_status = previous_status
        order.my_load_status.current_status = current_status
        order.my_load_status.next_status = next_status
        order.my_load_status.save()

        if current_status == SubStatus.DELIVERED:
            order.status = "CHECKOUT"
        elif current_status == SubStatus.PAID_OFF:
            order.status = "COMPLETED"
        elif current_status < SubStatus.DELIVERED and order.status != "ACTIVE":
            order.status = "ACTIVE"
        elif current_status < SubStatus.PAID_OFF and order.status != "ACTIVE":
            order.status = "CHECKOUT"

        order.save()

        return self.serializer(order.my_load_status).data

    def next_status(self, data):
        order = self._get_order(data)
        current_status = order.my_load_status.current_status

        if current_status < SubStatus.PAID_OFF:
            return self._update_status(order, current_status + 1), status.HTTP_200_OK
        else:
            return {"detail": "Cannot update status."}, status.HTTP_400_BAD_REQUEST

    def previous_status(self, data):
        order = self._get_order(data)
        current_status = order.my_load_status.current_status

        if current_status > SubStatus.POINT_A:
            return self._update_status(order, current_status - 1), status.HTTP_200_OK
        else:
            return {"detail": "Cannot update status."}, status.HTTP_400_BAD_REQUEST
