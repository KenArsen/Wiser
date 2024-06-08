import abc

from apps.order.models import Order


class ICreateOrderService(abc.ABC):
    @abc.abstractmethod
    def create(self, data, user) -> Order: ...


class IUpdateOrderService(abc.ABC):
    @abc.abstractmethod
    def update(self, order, data) -> Order: ...


class IDeleteOrderService(abc.ABC):
    @abc.abstractmethod
    def delete(self, order) -> None: ...


class IRefuseOrderService(abc.ABC):
    @abc.abstractmethod
    def refuse(self, order) -> None: ...


class IAssignOrderService(abc.ABC):
    @abc.abstractmethod
    def assign(self, data): ...
