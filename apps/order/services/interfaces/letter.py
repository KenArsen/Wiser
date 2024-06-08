import abc

from apps.order.models import Letter


class ICreateLetterService(abc.ABC):
    @abc.abstractmethod
    def create(self, data, user) -> Letter: ...


class IUpdateLetterService(abc.ABC):
    @abc.abstractmethod
    def update(self, letter, data) -> Letter: ...


class IDeleteOrderService(abc.ABC):
    @abc.abstractmethod
    def delete(self, letter) -> None: ...


class ISendLetterService(abc.ABC):
    @abc.abstractmethod
    def send_letter(self, data, user) -> None: ...
