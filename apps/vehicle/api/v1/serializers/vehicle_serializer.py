from rest_framework import serializers

from apps.vehicle.models import Location, Vehicle


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        ref_name = "Location"


class VehicleListSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False, read_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"
        ref_name = "VehicleList"


class VehicleDetailSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False, read_only=True)

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
