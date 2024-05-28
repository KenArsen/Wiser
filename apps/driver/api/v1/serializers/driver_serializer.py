from rest_framework import serializers

from apps.driver.models import Driver


class DriverListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"
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
