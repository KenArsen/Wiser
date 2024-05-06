from apps.order.models import MyLoadStatus, Order


class MyBidService:
    def __init__(self, order: Order) -> None:
        self.order = order

    def get_bids_yes(self):
        self.order.order_status = "ASSIGN"
        self.order.my_load_status.current_status = MyLoadStatus.Status.POINT_A
        self.order.my_load_status.next_status = MyLoadStatus.Status.UPLOADED
        self.order.my_load_status.save()
        self.order.save()

    def get_bids_no(self):
        self.order.is_active = False
        self.order.order_status = "REFUSED"
        self.order.save()
