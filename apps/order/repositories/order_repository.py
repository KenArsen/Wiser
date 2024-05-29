from rest_framework.exceptions import ValidationError

from apps.order.models import Order


class OrderRepository:
    def __init__(self, queryset):
        self.queryset = queryset

    def get_orders(self) -> list:
        return self.queryset.order_by("-updated_at", "-id")

    def get_order(self, pk: int) -> Order:
        try:
            return self.queryset.get(pk=pk)
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})
