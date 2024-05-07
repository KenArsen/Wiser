from apps.order.models import Order


class MyLoadRepository:
    @classmethod
    def get_all(cls, **kwargs) -> list:
        orders = Order.objects.filter(order_status="ASSIGN")
        return orders

    @classmethod
    def get_all_history(cls, **kwargs) -> dict:
        orders = Order.objects.filter(order_status="REFUSED")
        return orders
