from rest_framework import serializers

from apps.letter.api.v1.serializers import LetterReadSerializer
from apps.order.models import Assign, MyLoadStatus, Order


class MyLoadStatusSerializer(serializers.ModelSerializer):
    previous_status = serializers.CharField(source="get_previous_status_display")
    current_status = serializers.CharField(source="get_current_status_display")
    next_status = serializers.CharField(source="get_next_status_display")

    class Meta:
        model = MyLoadStatus
        fields = ("previous_status", "current_status", "next_status")


class AssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assign
        fields = ("order_id", "broker_company", "rate_confirmation")


class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = (
            "created_at",
            "updated_at",
            "order_status",
        )
        ref_name = "OrderWrite"

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


class OrderReadSerializer(serializers.ModelSerializer):
    my_load_status = MyLoadStatusSerializer(many=False, read_only=True)
    letter = LetterReadSerializer(required=False, read_only=True)
    assign = AssignSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "my_load_status", "order_status")
        ref_name = "OrderRead"
