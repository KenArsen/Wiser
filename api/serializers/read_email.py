from django.utils import dateformat
from rest_framework import serializers

from apps.read_email.models import Order


class OrderSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ('created',)

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.full_clean()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.full_clean()
        return instance

    def get_created_time(self, obj):
        formatted_time = dateformat.format(obj.created, 'h:i A')
        return formatted_time