from rest_framework.exceptions import ValidationError

from apps.order.models import MyLoadStatus

from .order_service import OrderService


class MyBidService(OrderService):
    def _get_order(self, data):
        order_id = data.get("order_id", None)
        if order_id is None:
            raise ValidationError({"detail": "order_id field is required."})
        order = self.repository.get_order(pk=order_id)
        return order

    def assign(self, data):
        order = self._get_order(data=data)
        order.order_status = "ASSIGN"
        order.my_load_status.current_status = MyLoadStatus.Status.POINT_A
        order.my_load_status.next_status = MyLoadStatus.Status.UPLOADED
        order.my_load_status.save()
        order.save()
        if hasattr(order, "assign"):
            order.assign.delete()
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError({"error": "Broker company/Rate confirmation not is valid"})
        return {"detail": "The order has been moved to My Loads"}

    def refuse(self, data):
        order = self._get_order(data=data)
        order.is_active = False
        order.order_status = "REFUSED"
        order.save()
        return {"detail": "The order has been moved to HISTORY"}
