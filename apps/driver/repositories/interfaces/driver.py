import abc
from typing import Any

from django.db.models.query import QuerySet

from apps.driver.models import Driver


class IDriverRepository(abc.ABC):
    @abc.abstractmethod
    def retrieve(self, pk: int) -> Driver: ...

    @abc.abstractmethod
    def create(self, data: dict[str, Any]) -> Driver: ...

    @abc.abstractmethod
    def update(self, driver: Driver, data: dict[str, Any]) -> Driver: ...

    @abc.abstractmethod
    def delete(self, driver: Driver) -> None: ...

    @abc.abstractmethod
    def list(self) -> QuerySet[Driver]: ...

    @abc.abstractmethod
    def get_all_active_drivers(self) -> QuerySet[Driver]: ...

    @abc.abstractmethod
    def get_all_inactive_drivers(self) -> QuerySet[Driver]: ...

    @abc.abstractmethod
    def none(self) -> QuerySet[Driver]: ...
