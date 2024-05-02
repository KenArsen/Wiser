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

    def validate(self, attrs):
        if not attrs.get("order_id"):
            raise serializers.ValidationError({"error": "Order ID is required."})
        if not attrs.get("driver_id"):
            raise serializers.ValidationError({"error": "Driver ID is required."})
        if not attrs.get("comment"):
            raise serializers.ValidationError({"error": "Comment is required."})
        return attrs
