from rest_framework import serializers

from apps.order.models import Order

from .common_serializer import MyLoadStatusSerializer


class MyLoadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "order_number",
            "status",
            "broker",
            "pick_up_location",
            "delivery_location",
        )
        ref_name = "MyLoadList"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        letter = getattr(instance, "letter", None)
        dispatcher = getattr(letter, "dispatcher", None) if letter else None

        representation["dispatcher"] = (
            f"{dispatcher.first_name} {dispatcher.last_name}" or None
        )

        return representation


class MyLoadDetailSerializer(serializers.ModelSerializer):
    my_load_status = MyLoadStatusSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "MyLoadDetail"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        letter = getattr(instance, "letter", None)
        driver = getattr(letter, "driver", None) if letter else None

        representation["broker_price"] = letter.broker_price or None
        representation["driver_price"] = letter.driver_price or None
        representation["driver_name"] = (
            f"{driver.first_name} {driver.last_name}" or None
        )
        representation["driver_phone"] = driver.phone_number or None
        representation["driver_email"] = driver.email or None

        return representation
