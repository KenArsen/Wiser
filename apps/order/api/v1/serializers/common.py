from django.db.models import Q
from rest_framework import serializers

from apps.order.models import Assign, Letter, MyLoadStatus, Order, Template


class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = (
            "id",
            "order",
            "driver",
            "comment",
            "broker_price",
            "driver_price",
        )
        read_only_fields = ("id",)
        ref_name = "Letter"

    def is_valid(self, raise_exception=False):
        order_id = self.initial_data.get("order")
        try:
            order = Order.objects.get(id=order_id)
            if order and hasattr(order, "letter"):
                order.letter.delete()

            return super().is_valid(raise_exception=raise_exception)
        except Order.DoesNotExist:
            pass


class RefuseSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.filter(Q(status="COMPLETED") | Q(status="CHECKOUT") | Q(status="ACTIVE")),
        write_only=True,
    )

    class Meta:
        model = Order
        fields = ("order",)


class MyLoadStatusSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.filter(Q(status="COMPLETED") | Q(status="CHECKOUT") | Q(status="ACTIVE")),
        write_only=True,
    )
    previous_status = serializers.CharField(source="get_previous_status_display", read_only=True)
    current_status = serializers.CharField(source="get_current_status_display", read_only=True)
    next_status = serializers.CharField(source="get_next_status_display", read_only=True)

    class Meta:
        model = MyLoadStatus
        fields = ("order", "previous_status", "current_status", "next_status")


class AssignSerializer(serializers.ModelSerializer):
    broker_price = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    driver_price = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    class Meta:
        model = Assign
        fields = ("id", "order", "broker_company", "rate_confirmation", "broker_price", "driver_price")
        read_only_fields = ("id",)

    def is_valid(self, raise_exception=False):
        order_id = self.initial_data.get("order")
        try:
            order = Order.objects.get(id=order_id)
            if order and hasattr(order, "assign"):
                order.assign.delete()

            return super().is_valid(raise_exception=raise_exception)
        except Order.DoesNotExist:
            pass

    def validate(self, data):
        broker_price = data.get("broker_price")
        driver_price = data.get("driver_price")

        if broker_price is not None and broker_price <= 0:
            raise serializers.ValidationError({"broker_price": "Broker price must be a positive value."})

        if driver_price is not None and driver_price <= 0:
            raise serializers.ValidationError({"driver_price": "Driver price must be a positive value."})

        return data


class TemplateSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Template
        fields = ["id", "is_active", "content", "logo_url"]
        ref_name = "Template"

    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None
