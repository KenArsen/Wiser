import abc

from django.db.models.query import QuerySet

from apps.order.models import Assign


class IAssignRepository(abc.ABC):
    @abc.abstractmethod
    def list(self) -> QuerySet[Assign]: ...

    @abc.abstractmethod
    def get_by_id(self, pk) -> Assign: ...

    @abc.abstractmethod
    def create(self, data) -> Assign: ...

    @abc.abstractmethod
    def update(self, assign, data) -> Assign: ...

    @abc.abstractmethod
    def delete(self, assign): ...

    @abc.abstractmethod
    def none(self) -> QuerySet[Assign]: ...
