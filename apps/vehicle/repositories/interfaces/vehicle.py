import abc
from typing import Any, Optional

from django.db.models.query import QuerySet

from apps.vehicle.models import Vehicle


class IVehicleRepository(abc.ABC):
    @abc.abstractmethod
    def retrieve(self, pk: Any) -> Vehicle: ...

    @abc.abstractmethod
    def create(self, data: dict[str, Any]) -> Vehicle: ...

    @abc.abstractmethod
    def update(self, vehicle: Vehicle, data: dict[str, Any]) -> Vehicle: ...

    @abc.abstractmethod
    def delete(self, vehicle: Vehicle) -> None: ...

    @abc.abstractmethod
    def list(self) -> QuerySet[Vehicle]: ...

    @abc.abstractmethod
    def get_by_unit_id(self, unit_id: str) -> Optional[Vehicle]: ...

    @abc.abstractmethod
    def get_all_active_vehicles(self) -> QuerySet[Vehicle]: ...

    @abc.abstractmethod
    def get_all_inactive_vehicles(self) -> QuerySet[Vehicle]: ...

    @abc.abstractmethod
    def none(self) -> QuerySet[Vehicle]: ...
