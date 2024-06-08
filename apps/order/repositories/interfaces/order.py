import abc

from django.db.models.query import QuerySet

from apps.order.models import Order


class OrderBaseRepository(abc.ABC):
    @abc.abstractmethod
    def list(self) -> list[Order]: ...

    @abc.abstractmethod
    def get_by_id(self, pk) -> Order: ...

    @abc.abstractmethod
    def none(self) -> QuerySet[Order]: ...


class IOrderRepository(OrderBaseRepository):
    @abc.abstractmethod
    def create(self, data, user) -> Order: ...

    @abc.abstractmethod
    def update(self, order, data) -> Order: ...

    @abc.abstractmethod
    def delete(self, order): ...

    @abc.abstractmethod
    def refuse(self, order): ...


class IloadBoardRepository(OrderBaseRepository, abc.ABC):
    pass


class IMyBidRepository(OrderBaseRepository):
    @abc.abstractmethod
    def history_list(self) -> list[Order]: ...


class IMyLoadRepository(OrderBaseRepository):
    @abc.abstractmethod
    def history_list(self) -> list[Order]: ...

    @abc.abstractmethod
    def checkout_list(self) -> list[Order]: ...

    @abc.abstractmethod
    def completed_list(self) -> list[Order]: ...

    @abc.abstractmethod
    def get_by_id_for_my_load_status(self, pk) -> Order: ...
