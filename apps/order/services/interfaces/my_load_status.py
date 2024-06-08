import abc

from apps.order.models import MyLoadStatus


class IMyLoadStatusService(abc.ABC):
    @abc.abstractmethod
    def create(self, data, order) -> MyLoadStatus: ...


class IMyLoadNextStatusService(abc.ABC):
    @abc.abstractmethod
    def next_status(self, data) -> MyLoadStatus: ...


class IMyLoadPreviousStatusService(abc.ABC):
    @abc.abstractmethod
    def previous_status(self, data) -> MyLoadStatus: ...
