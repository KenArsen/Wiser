from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.common.enums import SubStatus

from .order_service import OrderService


class MyLoadService(OrderService):

    def _get_order(self, data):
        order_id = data.get("order", None)
        if order_id is None:
            raise ValidationError({"detail": "order field is required."})
        order = self.get_order(pk=order_id)
        return order

    def next_status(self, data):
        order = self._get_order(data)
        current_status = order.my_load_status.current_status

        if current_status < SubStatus.PAID_OFF:
            order.my_load_status.previous_status = current_status
            order.my_load_status.current_status = current_status + 1
            order.my_load_status.next_status = current_status + 2
            order.my_load_status.save()

            if order.my_load_status.current_status == SubStatus.DELIVERED:
                order.status = "CHECKOUT"
            elif order.my_load_status.current_status == SubStatus.PAID_OFF:
                order.status = "COMPLETED"

            order.save()

            serializer = self.serializer(order.my_load_status)
            return serializer.data, status.HTTP_200_OK
        else:
            return {"message": "Cannot update status."}, status.HTTP_400_BAD_REQUEST

    def previous_status(self, data):
        order = self._get_order(data)
        current_status = order.my_load_status.current_status

        if current_status > SubStatus.POINT_A:
            order.my_load_status.next_status = current_status
            order.my_load_status.current_status = current_status - 1
            if current_status - 2 == 0:
                order.my_load_status.previous_status = None
            else:
                order.my_load_status.previous_status = current_status - 2
            order.my_load_status.save()

            if (
                order.my_load_status.current_status < SubStatus.DELIVERED
                and order.status != "ACTIVE"
            ):
                order.status = "ACTIVE"
            elif (
                order.my_load_status.current_status < SubStatus.PAID_OFF
                and order.status != "ACTIVE"
            ):
                order.status = "CHECKOUT"

            order.save()

            serializer = self.serializer(order.my_load_status)
            return serializer.data, status.HTTP_200_OK
        else:
            return {"message": "Cannot update status."}, status.HTTP_400_BAD_REQUEST
