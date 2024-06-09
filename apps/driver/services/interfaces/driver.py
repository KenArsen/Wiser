import abc
from typing import Any


class IDriverCreateService(abc.ABC):
    @abc.abstractmethod
    def create(self, data: dict[str, Any]) -> Any: ...


class IDriverUpdateService(abc.ABC):
    @abc.abstractmethod
    def update(self, driver: Any, data: dict[str, Any]) -> Any: ...


class IDriverDeleteService(abc.ABC):
    @abc.abstractmethod
    def delete(self, driver: Any) -> None: ...


class IDriverActivateService(abc.ABC):
    @abc.abstractmethod
    def activate(self, driver: Any) -> None: ...


class IDriverDeactivateService(abc.ABC):
    @abc.abstractmethod
    def deactivate(self, driver: Any) -> None: ...
