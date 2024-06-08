from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError

from apps.order.models import Assign
from apps.order.repositories.interfaces.assign import IAssignRepository


class AssignRepository(IAssignRepository):
    def get_by_id(self, pk) -> Assign:
        try:
            return Assign.objects.get(id=pk)
        except Assign.DoesNotExist:
            raise ValidationError({"detail": "Assign not found"})

    def create(self, data) -> Assign:
        return Assign.objects.create(**data)

    def update(self, assign, data) -> Assign:
        for key, value in data.items():
            setattr(assign, key, value)
        assign.save()
        return assign

    def delete(self, assign) -> None:
        assign.delete()

    def none(self) -> QuerySet[Assign]:
        return Assign.objects.none()

    def list(self) -> list[Assign]:
        return Assign.objects.filter().order_by("-updated_at", "-id")
