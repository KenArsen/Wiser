import abc
from typing import List, Union

from django.db.models.query import QuerySet

from apps.order.models import MyLoadStatus, Order


class IMyLoadStatusRepository(abc.ABC):
    @abc.abstractmethod
    def list_statuses(self) -> List[MyLoadStatus]: ...

    @abc.abstractmethod
    def retrieve_status(self, pk) -> Union[MyLoadStatus, None]: ...

    @abc.abstractmethod
    def create_status(self, order: Order, data: dict) -> MyLoadStatus: ...

    @abc.abstractmethod
    def update_status(self, order: Order, data: dict) -> MyLoadStatus: ...

    @abc.abstractmethod
    def delete_status(self, order: Order) -> None: ...

    @abc.abstractmethod
    def none(self) -> QuerySet[MyLoadStatus]: ...
