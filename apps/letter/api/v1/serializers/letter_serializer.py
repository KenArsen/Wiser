from rest_framework import serializers

from apps.letter.models import Letter


class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ("id", "comment")


class LetterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ("id", "order_id", "driver_id", "comment")
        read_only_fields = ("id",)
