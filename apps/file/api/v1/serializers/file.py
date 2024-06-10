from rest_framework import serializers

from apps.file.models import File


class WriteFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
        read_only_fields = ("id",)
        ref_name = "WriteFile"


class ReadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
        read_only_fields = ("id",)
        ref_name = "ReadFile"
