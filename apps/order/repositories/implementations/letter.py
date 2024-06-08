from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from apps.order.models import Letter
from apps.order.repositories.interfaces.letter import ILetterRepository


class LetterRepository(ILetterRepository):
    def list(self) -> list[Letter]:
        return Letter.objects.filter()

    def get_by_id(self, pk) -> Letter:
        try:
            return Letter.objects.get(id=pk)
        except Letter.DoesNotExist:
            raise ValidationError({"detail": "Letter not found"})

    def create(self, data) -> Letter:
        return Letter.objects.create(**data)

    def update(self, letter, data) -> Letter:
        for key, value in data.items():
            setattr(letter, key, value)
        letter.save()
        return letter

    def delete(self, letter):
        letter.delete()

    def none(self) -> QuerySet[Letter]:
        return Letter.objects.none()
