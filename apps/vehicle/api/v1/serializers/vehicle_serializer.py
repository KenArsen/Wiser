from rest_framework import serializers

from apps.vehicle.models import Vehicles


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
