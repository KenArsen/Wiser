from rest_framework import serializers

from apps.order.models import Assign, File, MyLoadStatus


class MyLoadStatusSerializer(serializers.ModelSerializer):
    previous_status = serializers.CharField(source="get_previous_status_display")
    current_status = serializers.CharField(source="get_current_status_display")
    next_status = serializers.CharField(source="get_next_status_display")

    class Meta:
        model = MyLoadStatus
        fields = ("previous_status", "current_status", "next_status")


class AssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assign
        fields = ("order", "broker_company", "rate_confirmation")


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
        ref_name = "File"
