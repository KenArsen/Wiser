import abc
from typing import List, Optional

from django.db.models.query import QuerySet

from apps.order.models import Letter


class ILetterRepository(abc.ABC):
    @abc.abstractmethod
    def list_letters(self) -> List[Letter]:
        """Retrieve a list of all letters."""
        ...

    @abc.abstractmethod
    def retrieve_letter(self, pk: int) -> Optional[Letter]:
        """Retrieve a letter by its primary key."""
        ...

    @abc.abstractmethod
    def create_letter(self, data: dict) -> Letter:
        """Create a new letter."""
        ...

    @abc.abstractmethod
    def update_letter(self, letter: Letter, data: dict) -> Letter:
        """Update an existing letter."""
        ...

    @abc.abstractmethod
    def delete_letter(self, letter: Letter) -> None:
        """Delete a letter."""
        ...

    @abc.abstractmethod
    def none(self) -> QuerySet[Letter]:
        """Return an empty queryset of letters."""
        ...
