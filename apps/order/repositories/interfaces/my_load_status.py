import abc

from django.db.models.query import QuerySet

from apps.order.models import MyLoadStatus


class IMyLoadStatusRepository(abc.ABC):
    @abc.abstractmethod
    def list(self) -> list[MyLoadStatus]: ...

    @abc.abstractmethod
    def get_by_id(self, pk) -> MyLoadStatus: ...

    @abc.abstractmethod
    def create(self, order, data) -> MyLoadStatus: ...

    @abc.abstractmethod
    def update(self, order, data) -> MyLoadStatus: ...

    @abc.abstractmethod
    def delete(self, order): ...

    @abc.abstractmethod
    def none(self) -> QuerySet[MyLoadStatus]: ...
