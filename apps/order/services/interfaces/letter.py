import abc

from apps.order.models import Letter


class ICreateLetterService(abc.ABC):
    @abc.abstractmethod
    def create_letter(self, data, user) -> Letter: ...


class IUpdateLetterService(abc.ABC):
    @abc.abstractmethod
    def update_letter(self, letter, data) -> Letter: ...


class IDeleteLetterService(abc.ABC):
    @abc.abstractmethod
    def delete_letter(self, letter) -> None: ...


class ISendLetterService(abc.ABC):
    @abc.abstractmethod
    def send_letter(self, data, user) -> None: ...
