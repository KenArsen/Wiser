from rest_framework import serializers

from apps.order.models import Letter, Price


class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ("id", "order", "driver", "comment", "dispatcher")
        ref_name = "Letter"


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ("id", "order", "driver", "dispatcher", "broker_price", "driver_price")
        ref_name = "Price"
