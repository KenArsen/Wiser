from typing import Any

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from apps.driver.models import Driver

from ..interfaces.driver import IDriverRepository


class DriverRepository(IDriverRepository):
    def retrieve(self, pk: int) -> Driver:
        try:
            return Driver.objects.get(id=pk)
        except Driver.DoesNotExist:
            raise ValidationError({"detail": "Driver not found"})

    def create(self, data: dict[str, Any]) -> Driver:
        return Driver.objects.create(**data)

    def update(self, driver: Driver, data: dict[str, Any]) -> Driver:
        for key, value in data.items():
            setattr(driver, key, value)
        driver.save()
        return driver

    def delete(self, driver: Driver) -> None:
        driver.delete()

    def list(self) -> QuerySet[Driver]:
        return Driver.objects.all()

    def get_all_active_drivers(self) -> QuerySet[Driver]:
        return Driver.objects.active()

    def get_all_inactive_drivers(self) -> QuerySet[Driver]:
        return Driver.objects.inactive()

    def none(self) -> QuerySet[Driver]:
        return Driver.objects.none()
