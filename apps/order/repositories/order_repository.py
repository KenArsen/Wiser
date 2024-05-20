from rest_framework.exceptions import ValidationError

from apps.order.models import Order


class OrderRepository:
    @classmethod
    def get_orders(cls) -> list:
        return Order.objects.all().order_by("-updated_at", "-id")

    @classmethod
    def get_filtered_orders(cls, **kwargs) -> list:
        return Order.objects.filter(**kwargs).order_by("-updated_at", "-id")

    @classmethod
    def get_order(cls, pk: int) -> Order:
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})
