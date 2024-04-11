from django.utils import dateformat
from rest_framework import serializers

from apps.letter.api.v1.serializers import LetterReadSerializer
from apps.order.models import Assign, Order


class AssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assign
        fields = ("broker_company", "rate_confirmation")


class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = (
            "created_at",
            "updated_at",
            "is_active",
            "order_status",
            "my_loads_status",
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
    created_time = serializers.SerializerMethodField(read_only=True)
    my_loads_status = serializers.CharField(source="get_my_loads_status_display", read_only=True)
    letter = LetterReadSerializer(required=False, read_only=True)
    assign = AssignSerializer(read_only=True)

    class Meta:
        model = Order
        exclude = (
            "created_at",
            "updated_at",
        )
        ref_name = "OrderRead"

    def get_created_time(self, obj):
        formatted_time = dateformat.format(obj.created_at, "h:i A")
        return formatted_time


class OrderSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField(read_only=True)
    my_loads_status = serializers.CharField(source="get_my_loads_status_display", read_only=True)
    letter = LetterReadSerializer(required=False, read_only=True)
    assign = AssignSerializer(read_only=True)

    class Meta:
        model = Order
        read_only_fields = ["is_active", "order_status"]
        exclude = (
            "created_at",
            "updated_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["letter"] is None:
            del data["letter"]
        if data["assign"] is None:
            del data["assign"]
        return data

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
