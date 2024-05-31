from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.order.models import Order
from apps.order.repositories import OrderRepository


class OrderService(OrderRepository):
    def __init__(self, serializer, queryset):
        super().__init__(queryset=queryset)
        self.serializer = serializer

    def update_order(self, instance, data, partial=False):
        serializer = self.serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_order(self, instance):
        if instance.user:
            instance.status = "EXPIRED"
        else:
            instance.delete()
            return {"detail": "Order deleted successfully."}
        instance.save()
        return {"detail": "This order has been marked as inactive."}

    def refuse_order(self, order_id):
        try:
            with transaction.atomic():
                instance = self.get_order(pk=order_id)
                instance.status = "REFUSED"
                instance.save()
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})
        return {"detail": "The order has been moved to HISTORY"}
