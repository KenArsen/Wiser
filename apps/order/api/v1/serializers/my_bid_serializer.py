from rest_framework import serializers

from apps.order.models import Order

from . import LetterSerializer


class MyBidListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "order_number",
            "broker",
            "pick_up_location",
            "delivery_location",
        )
        ref_name = "MyBidDetail"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        letter = getattr(instance, "letter", None)
        dispatcher = getattr(letter, "dispatcher", None)

        representation["pick_up_coordinate"] = (
            f"{instance.pick_up_latitude},{instance.pick_up_longitude}"
        )
        representation["delivery_coordinate"] = (
            f"{instance.delivery_latitude},{instance.delivery_longitude}"
        )

        representation["broker_price"] = letter.broker_price or None
        representation["dispatcher"] = (
            f"{dispatcher.first_name} {dispatcher.last_name}" or None
        )
        representation["dispatcher_phone"] = dispatcher.phone_number or None

        return representation


class MyBidDetailSerializer(serializers.ModelSerializer):
    letter = LetterSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "MyBidDetail"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        letter = getattr(instance, "letter", None)
        dispatcher = getattr(letter, "dispatcher", None) if letter else None
        driver = getattr(letter, "driver", None) if letter else None

        representation["broker_price"] = letter.broker_price or None
        representation["driver_price"] = letter.driver_price or None
        representation["dispatcher"] = (
            f"{dispatcher.first_name} {dispatcher.last_name}" or None
        )
        representation["driver"] = f"{driver.first_name} {driver.last_name}" or None
        representation["dispatcher_phone"] = dispatcher.phone_number or None
        representation["dispatcher_email"] = dispatcher.email or None

        return representation


class MyBidHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("id", "created_at", "order_number", "broker", "status")
        ref_name = "MyBidHistory"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        letter = getattr(instance, "letter", None)
        dispatcher = getattr(letter, "dispatcher", None) if letter else None

        representation["broker_price"] = letter.broker_price if letter else None
        representation["dispatcher"] = (
            f"{dispatcher.first_name} {dispatcher.last_name}" if dispatcher else None
        )

        return representation
