from django.db import transaction

from apps.order.models import Order
from apps.order.repositories.implementations.my_load_status import (
    MyLoadStatusRepository,
)
from apps.order.repositories.interfaces.assign import IAssignRepository
from apps.order.repositories.interfaces.order import IOrderRepository
from apps.order.services.interfaces.order import (
    IAssignOrderService,
    ICreateOrderService,
    IDeleteOrderService,
    IRefuseOrderService,
    IUpdateOrderService,
)


class CreateOrderService(ICreateOrderService):
    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository

    def create(self, data, user) -> Order:
        return self.order_repository.create(data, user)


class UpdateOrderService(IUpdateOrderService):
    def __init__(self, order_repository: IOrderRepository):
        self._order_repository = order_repository

    def update(self, order, data) -> Order:
        return self._order_repository.update(order, data)


class DeleteOrderService(IDeleteOrderService):
    def __init__(self, order_repository: IOrderRepository):
        self._order_repository = order_repository

    def delete(self, order) -> Order:
        return self._order_repository.delete(order)


class RefuseOrderService(IRefuseOrderService):
    def __init__(self, order_repository: IOrderRepository):
        self._order_repository = order_repository

    def refuse(self, order):
        self._order_repository.refuse(order)


class AssignOrderService(IAssignOrderService):
    def __init__(self, assign_repository: IAssignRepository):
        self._assign_repository = assign_repository

    def assign(self, data):
        order = data.get("order", None)
        with transaction.atomic():
            order.status = "ACTIVE"
            order.save(update_fields=["status", "updated_at"])

            MyLoadStatusRepository().create(data=data, order=order)

            broker_price = data.pop("broker_price", None)
            driver_price = data.pop("driver_price", None)

            if broker_price is not None:
                order.letter.broker_price = broker_price
                order.letter.save(update_fields=["broker_price", "updated_at"])

            if driver_price is not None:
                order.letter.driver_price = driver_price
                order.letter.save(update_fields=["driver_price", "updated_at"])

            self._assign_repository.create(data)
