from django.db.models import Q
from rest_framework import serializers

from apps.order.models import Assign, File, Letter, MyLoadStatus, Order, Template


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
    class Meta:
        model = Assign
        fields = ("id", "order", "broker_company", "rate_confirmation")
        read_only_fields = ("id",)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
        ref_name = "File"


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
