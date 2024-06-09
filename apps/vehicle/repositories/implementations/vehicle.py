from typing import Any, Optional

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from apps.vehicle.models import Vehicle

from ..interfaces.vehicle import IVehicleRepository


class VehicleRepository(IVehicleRepository):
    def retrieve(self, pk: Any) -> Vehicle:
        try:
            return Vehicle.objects.get(id=pk)
        except Vehicle.DoesNotExist:
            raise ValidationError({"detail": "Vehicle not found"})

    def create(self, data: dict[str, Any]) -> Vehicle:
        return Vehicle.objects.create(**data)

    def update(self, vehicle: Vehicle, data: dict[str, Any]) -> Vehicle:
        for key, value in data.items():
            setattr(vehicle, key, value)
        vehicle.save()
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        vehicle.delete()

    def list(self) -> QuerySet[Vehicle]:
        return Vehicle.objects.all()

    def get_by_unit_id(self, unit_id: str) -> Optional[Vehicle]:
        try:
            return Vehicle.objects.get(unit_id=unit_id)
        except Vehicle.DoesNotExist:
            return None

    def get_all_active_vehicles(self) -> QuerySet[Vehicle]:
        return Vehicle.objects.active()

    def get_all_inactive_vehicles(self) -> QuerySet[Vehicle]:
        return Vehicle.objects.inactive()

    def none(self) -> QuerySet[Vehicle]:
        return Vehicle.objects.none()
