from rest_framework import serializers

from apps.read_email.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('user',)
