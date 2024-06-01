from rest_framework import serializers

from apps.vehicle.models import Vehicle


class VehicleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ("id", "unit_id", "transport_type", "vehicle_model", "vin", "driver", "dispatcher", "owner")
        ref_name = "VehicleList"


class VehicleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
        ref_name = "VehicleDetail"


class VehicleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
        ref_name = "VehicleCreate"


class VehicleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
        ref_name = "VehicleUpdate"
