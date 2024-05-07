from rest_framework.exceptions import ValidationError

from apps.order.models import Order


class OrderRepository:
    @classmethod
    def get_orders(cls) -> list:
        return Order.objects.all()

    @classmethod
    def get_filter(cls, **kwargs) -> list:
        return Order.objects.filter(**kwargs)

    @classmethod
    def get_order(cls, pk: int) -> Order:
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})

    @classmethod
    def get_orders_by_status(cls, status_: str, order_by_=None) -> list:
        if order_by_ is None:
            return Order.objects.filter(order_status=status_)
        return Order.objects.filter(order_status=status_).order_by(order_by_)
