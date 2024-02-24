from django.utils import dateformat
from rest_framework import serializers

from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = (
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        instance = Order(**validated_data)
        instance.full_clean()  # Вызов метода clean()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()  # Вызов метода clean()
        instance.save()
        return instance

    def get_created_time(self, obj):
        formatted_time = dateformat.format(obj.created_at, "h:i A")
        return formatted_time
