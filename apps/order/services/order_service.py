from rest_framework.exceptions import ValidationError

from apps.common.nominatim import create_point, get_location
from apps.order.models import Point
from apps.order.repositories import OrderRepository


class OrderService:
    repository = OrderRepository

    def __init__(self, serializer):
        self.serializer = serializer

    def get_order(self, pk):
        return self.repository.get_order(pk=pk)

    def get_filtered_orders(self, **kwargs):
        return self.repository.get_filtered_orders(**kwargs)

    def get_orders(self):
        return self.repository.get_orders()

    def create_order(self, data):
        pick_up_at = data.pop("pick_up_at")
        pick_up_date = data.pop("pick_up_date")
        deliver_to = data.pop("deliver_to")
        deliver_date = data.pop("deliver_date")

        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            create_point(serializer.instance, pick_up_at, pick_up_date, "PICK_UP")
            create_point(serializer.instance, deliver_to, deliver_date, "DELIVER_TO")
            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    def update_order(self, instance, data, partial=False):
        serializer = self.serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_order(self, instance):
        if instance.user:
            instance.status = "EXPIRED"
            instance.save()
            return {"detail": "This order has been marked as inactive."}
        else:
            instance.delete()
            return {"detail": "Order deleted successfully."}

    def order_refuse(self, order_id):
        instance = self.get_order(pk=order_id)
        instance.status = "REFUSED"
        instance.save()
        return {"detail": "The order has been moved to HISTORY"}
