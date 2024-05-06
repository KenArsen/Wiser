from apps.order.models import Order


class MyLoadRepository:
    @classmethod
    def get_my_loads(cls, **kwargs) -> list:
        orders = Order.objects.filter(order_status="ASSIGN")
        return orders

    @classmethod
    def get_my_loads_history(cls, **kwargs) -> dict:
        orders = Order.objects.filter(order_status="REFUSED")
        return orders
