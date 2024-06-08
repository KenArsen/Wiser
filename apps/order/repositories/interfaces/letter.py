import abc

from django.db.models.query import QuerySet

from apps.order.models import Letter


class ILetterRepository(abc.ABC):
    @abc.abstractmethod
    def list(self) -> list[Letter]: ...

    @abc.abstractmethod
    def get_by_id(self, pk) -> Letter: ...

    @abc.abstractmethod
    def create(self, data) -> Letter: ...

    @abc.abstractmethod
    def update(self, letter, data) -> Letter: ...

    @abc.abstractmethod
    def delete(self, letter): ...

    @abc.abstractmethod
    def none(self) -> QuerySet[Letter]: ...
