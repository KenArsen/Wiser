from rest_framework import serializers

from apps.driver.models import Driver


class DriverAvailabilityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("id", "is_available", "updated_at")
        read_only_fields = ("id", "is_available", "updated_at")
        ref_name = "DriverAvailabilityUpdate"


class DriverListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("id", "first_name", "last_name", "email", "phone_number", "ssn", "lisense_number")
        ref_name = "DriverList"


class DriverDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"
        ref_name = "DriverDetail"


class DriverCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"
        ref_name = "DriverCreate"


class DriverUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"
        ref_name = "DriverUpdate"
