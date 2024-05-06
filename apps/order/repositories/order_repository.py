from apps.order.models import Order


class OrderRepository:
    @classmethod
    def get_all(cls, **kwargs) -> list:
        orders = Order.objects.filter(**kwargs)
        return orders

    @classmethod
    def get_by_id(cls, pk: int) -> Order:
        return Order.objects.get(pk=pk)

    @staticmethod
    def get_by_status(status):
        return Order.objects.filter(order_status=status).order_by("-id")
