from rest_framework import serializers

from apps.letter.models import Letter


class LetterReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        exclude = ("updated_at",)
        ref_name = "LetterRead"


class LetterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
        ref_name = "LetterWrite"
