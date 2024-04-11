from rest_framework import serializers

from apps.driver.models import Driver


class DriverSerializers(serializers.ModelSerializer):
    class Meta:
        model = Driver
        read_only_fields = ("created_at", "updated_at", "is_active")
        fields = "__all__"
        ref_name = "Driver"
