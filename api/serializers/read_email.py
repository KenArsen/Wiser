from rest_framework import serializers
from django.utils import dateformat

from apps.read_email.models import Order


class OrderSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ('created',)

    def get_created_time(self, obj):
        formatted_time = dateformat.format(obj.created, 'h:i A')
        return formatted_time
