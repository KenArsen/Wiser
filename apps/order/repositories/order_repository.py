from rest_framework.exceptions import ValidationError

from apps.order.models import Order


class OrderRepository:
    @classmethod
    def get_orders(cls) -> list:
        return Order.objects.all()

    @classmethod
    def get_filtered_orders(cls, **kwargs) -> list:
        order_by_ = kwargs.pop("order_by_", None)
        if order_by_:
            return Order.objects.filter(**kwargs).order_by(order_by_)
        return Order.objects.filter(**kwargs)

    @classmethod
    def get_order(cls, pk: int) -> Order:
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})
