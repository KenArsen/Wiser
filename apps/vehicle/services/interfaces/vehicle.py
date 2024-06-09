import abc
from typing import Any


class IVehicleCreateService(abc.ABC):
    @abc.abstractmethod
    def create(self, data: dict[str, Any]) -> Any: ...


class IVehicleUpdateService(abc.ABC):
    @abc.abstractmethod
    def update(self, vehicle: Any, data: dict[str, Any]) -> Any: ...


class IVehicleDeleteService(abc.ABC):
    @abc.abstractmethod
    def delete(self, vehicle: Any) -> None: ...


class IVehicleActivateService(abc.ABC):
    @abc.abstractmethod
    def activate(self, vehicle: Any) -> None: ...


class IVehicleDeactivateService(abc.ABC):
    @abc.abstractmethod
    def deactivate(self, vehicle: Any) -> None: ...
