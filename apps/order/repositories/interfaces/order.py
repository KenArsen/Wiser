import abc
from typing import Any, List

from django.db.models.query import QuerySet

from apps.order.models import Order


class BaseOrderRepository(abc.ABC):
    @abc.abstractmethod
    def list_orders(self) -> List[Order]: ...

    @abc.abstractmethod
    def retrieve_order(self, pk: int) -> Order: ...

    @abc.abstractmethod
    def none(self) -> QuerySet[Order]: ...


class IOrderRepository(BaseOrderRepository):
    @abc.abstractmethod
    def create_order(self, data: dict, user: Any) -> Order: ...

    @abc.abstractmethod
    def update_order(self, order: Order, data: dict) -> Order: ...

    @abc.abstractmethod
    def delete_order(self, order: Order) -> None: ...

    @abc.abstractmethod
    def refuse_order(self, order: Order) -> None: ...


class ILoadBoardRepository(BaseOrderRepository, abc.ABC):
    pass


class IMyBidRepository(BaseOrderRepository):
    @abc.abstractmethod
    def get_history_orders(self) -> List[Order]: ...


class IMyLoadRepository(BaseOrderRepository):
    @abc.abstractmethod
    def get_order_for_update_substatus(self, pk) -> Order: ...
    @abc.abstractmethod
    def get_history_orders(self) -> List[Order]: ...

    @abc.abstractmethod
    def get_checkout_orders(self) -> List[Order]: ...

    @abc.abstractmethod
    def get_completed_orders(self) -> List[Order]: ...
