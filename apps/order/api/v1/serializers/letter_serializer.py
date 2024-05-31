from rest_framework import serializers

from apps.order.models import Letter


class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = (
            "id",
            "order",
            "driver",
            "comment",
            "broker_price",
            "driver_price",
        )
        ref_name = "Letter"
