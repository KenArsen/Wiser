from apps.order.models import Order


class MyBids:
    def __init__(self, order: Order) -> None:
        self.order = order

    def get_bids_yes(self):
        self.order.order_status = "MY_LOADS"
        self.order.save()

    def get_bids_no(self):
        self.order.is_active = False
        self.order.save()
