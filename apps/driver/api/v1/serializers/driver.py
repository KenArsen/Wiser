from rest_framework import serializers

from apps.driver.models import Driver
from apps.vehicle.models import Vehicle


class DriversVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ("id", "dispatcher", "owner", "location", "coordinate")


class DriverStatusSerializer(serializers.ModelSerializer):
    driver = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Driver
        fields = ("id", "is_active", "updated_at", "driver")
        read_only_fields = ("id", "is_active", "updated_at")
        ref_name = "DriverStatus"


class DriverListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("id", "first_name", "last_name", "email", "phone_number", "ssn", "license_number")
        ref_name = "DriverList"


class DriverDetailSerializer(serializers.ModelSerializer):
    vehicle = DriversVehicleSerializer(read_only=True)

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