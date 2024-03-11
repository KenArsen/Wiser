from django.utils import dateformat
from rest_framework import serializers

from apps.letter.api.v1.serializers import LetterSerializer
from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField(read_only=True)
    my_loads_status = serializers.CharField(source="get_my_loads_status_display", read_only=True)
    letter = LetterSerializer(read_only=True)

    class Meta:
        model = Order
        read_only_fields = ["is_active", "order_status"]
        exclude = (
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        instance = Order(**validated_data)
        instance.full_clean()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()
        instance.save()
        return instance

    def get_created_time(self, obj):
        formatted_time = dateformat.format(obj.created_at, "h:i A")
        return formatted_time
