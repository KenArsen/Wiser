from apps.order.models import Order


class MyBidRepository:
    @classmethod
    def get_my_bids(cls, **kwargs) -> list:
        orders = Order.objects.filter(order_status="AWAITING_BID")
        return orders

    @classmethod
    def get_my_bids_history(cls, **kwargs) -> dict:
        orders = Order.objects.filter(order_status="REFUSED")
        return orders
