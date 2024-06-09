from typing import Any

from apps.vehicle.repositories.interfaces.vehicle import IVehicleRepository

from ..interfaces.vehicle import (
    IVehicleActivateService,
    IVehicleCreateService,
    IVehicleDeactivateService,
    IVehicleDeleteService,
    IVehicleUpdateService,
)


class VehicleCreateService(IVehicleCreateService):
    def __init__(self, repository: IVehicleRepository):
        self._repository = repository

    def create(self, data: dict[str, Any]) -> Any:
        return self._repository.create(data)


class VehicleUpdateService(IVehicleUpdateService):
    def __init__(self, repository: IVehicleRepository):
        self._repository = repository

    def update(self, vehicle: Any, data: dict[str, Any]) -> Any:
        return self._repository.update(vehicle, data)


class VehicleDeleteService(IVehicleDeleteService):
    def __init__(self, repository: IVehicleRepository):
        self._repository = repository

    def delete(self, vehicle: Any) -> None:
        self._repository.delete(vehicle)


class VehicleActivateService(IVehicleActivateService):
    def __init__(self, repository: IVehicleRepository):
        self._repository = repository

    def activate(self, vehicle: Any) -> None:
        vehicle.activate()


class VehicleDeactivateService(IVehicleDeactivateService):
    def __init__(self, repository: IVehicleRepository):
        self._repository = repository

    def deactivate(self, vehicle: Any) -> None:
        vehicle.deactivate()
