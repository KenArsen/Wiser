from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from apps.order.models import Letter
from apps.order.repositories.interfaces.letter import ILetterRepository


class LetterRepository(ILetterRepository):
    def list_letters(self) -> QuerySet[Letter]:
        return Letter.objects.all()

    def retrieve_letter(self, pk: int) -> Letter:
        try:
            return Letter.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Letter.DoesNotExist("Letter not found")

    def create_letter(self, data: dict) -> Letter:
        return Letter.objects.create(**data)

    def update_letter(self, letter: Letter, data: dict) -> Letter:
        for key, value in data.items():
            setattr(letter, key, value)
        letter.save()
        return letter

    def delete_letter(self, letter: Letter) -> None:
        letter.delete()

    def none(self) -> QuerySet[Letter]:
        return Letter.objects.none()
