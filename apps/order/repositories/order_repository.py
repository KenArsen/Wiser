from apps.order.models import Order


class OrderRepository:
    @classmethod
    def get_order_list(cls, **kwargs) -> list:
        orders = Order.objects.filter(**kwargs)
        return orders
