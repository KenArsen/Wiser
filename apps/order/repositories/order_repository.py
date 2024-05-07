from apps.order.models import Order


class OrderRepository:
    @classmethod
    def get_all(cls) -> list:
        orders = Order.objects.all()
        return orders

    @classmethod
    def get_filter(cls, **kwargs) -> list:
        return Order.objects.filter(**kwargs)

    @classmethod
    def get_by_id(cls, pk: int) -> Order:
        return Order.objects.get(pk=pk)

    @classmethod
    def get_all_by_status(cls, status_: str, order_by_=None) -> list:
        if order_by_ is None:
            return Order.objects.filter(order_status=status_)
        else:
            return Order.objects.filter(order_status=status_).order_by(order_by_)
