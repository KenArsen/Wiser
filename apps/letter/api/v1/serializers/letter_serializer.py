from rest_framework import serializers

from apps.letter.models import Letter


class LetterReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        exclude = ("created_at", "updated_at")
        ref_name = "LetterRead"


class LetterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        exclude = ("created_at", "updated_at", "id")
        ref_name = "LetterWrite"
