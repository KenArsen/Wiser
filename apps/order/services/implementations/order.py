from typing import Dict

from django.db import transaction

from apps.order.models import Assign, Order
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
    def __init__(self, repository: IOrderRepository):
        self._repository = repository

    def create_order(self, data: Dict[str, any], user: any) -> Order:
        return self._repository.create_order(data, user)


class UpdateOrderService(IUpdateOrderService):
    def __init__(self, repository: IOrderRepository):
        self._repository = repository

    def update_order(self, order: Order, data: Dict[str, any]) -> Order:
        return self._repository.update_order(order, data)


class DeleteOrderService(IDeleteOrderService):
    def __init__(self, repository: IOrderRepository):
        self._repository = repository

    def delete_order(self, order: Order) -> None:
        self._repository.delete_order(order)


class RefuseOrderService(IRefuseOrderService):
    def __init__(self, repository: IOrderRepository):
        self._repository = repository

    def refuse_order(self, order: Order) -> None:
        self._repository.refuse_order(order)


class AssignOrderService(IAssignOrderService):
    def __init__(self, repository: IAssignRepository):
        self._repository = repository

    def assign_order(self, data: Dict[str, Order]) -> Assign:
        order = data.get("order", None)
        with transaction.atomic():
            order.status = "ACTIVE"
            order.save(update_fields=["status", "updated_at"])

            MyLoadStatusRepository().create_status(data=data, order=order)

            broker_price = data.pop("broker_price", None)
            driver_price = data.pop("driver_price", None)

            if broker_price is not None:
                order.letter.broker_price = broker_price
                order.letter.save(update_fields=["broker_price", "updated_at"])

            if driver_price is not None:
                order.letter.driver_price = driver_price
                order.letter.save(update_fields=["driver_price", "updated_at"])

            return self._repository.create(data)
