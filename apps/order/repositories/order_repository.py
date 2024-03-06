from apps.order.models import Order


class OrderRepository:
    @classmethod
    def get_order_list(cls, **kwargs) -> list:
        orders = Order.objects.filter(**kwargs)
        return orders

    @classmethod
    def get_order(cls, pk: int) -> Order:
        return Order.objects.get(pk=pk)
