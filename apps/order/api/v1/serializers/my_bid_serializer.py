from rest_framework import serializers

from apps.order.models import Order


class MyBidListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "status",
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
        dispatcher = instance.user or None

        coordinates = get_coordinates(instance)
        representation.update(coordinates)

        dispatcher_info = get_dispatcher_info(dispatcher)
        representation.update(dispatcher_info)

        representation["broker_price"] = letter.broker_price if letter else None

        return representation


class MyBidHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "created_at",
            "order_number",
            "broker",
            "status",
            "pick_up_location",
            "delivery_location",
        )
        ref_name = "MyBidHistory"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        letter = getattr(instance, "letter", None)
        dispatcher = instance.user

        coordinates = get_coordinates(instance)
        representation.update(coordinates)

        dispatcher_info = get_dispatcher_info(dispatcher)
        representation.update(dispatcher_info)

        representation["broker_price"] = letter.broker_price if letter else None

        return representation


class MyBidDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "status",
            "order_number",
            "pick_up_location",
            "pick_up_date",
            "delivery_location",
            "delivery_date",
            "stops",
            "broker",
            "broker_phone",
            "broker_email",
            "posted",
            "expires",
            "dock_level",
            "hazmat",
            "amount",
            "fast_load",
            "notes",
            "load_type",
            "vehicle_required",
            "pieces",
            "weight",
            "dimensions",
            "stackable",
        )
        ref_name = "MyBidDetail"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        dispatcher = instance.user

        coordinates = get_coordinates(instance)
        representation.update(coordinates)

        dispatcher_info = get_dispatcher_info(dispatcher)
        representation.update(dispatcher_info)

        letter = getattr(instance, "letter", None)

        if letter:
            representation["broker_price"] = letter.broker_price
            representation["driver_price"] = letter.driver_price
            representation["message"] = letter.comment
        else:
            representation["broker_price"] = None
            representation["driver_price"] = None
            representation["message"] = None

        return representation


def get_coordinates(instance):
    return {
        "pick_up_coordinate": (
            f"{instance.pick_up_latitude},{instance.pick_up_longitude}"
            if instance.pick_up_latitude and instance.pick_up_longitude
            else None
        ),
        "delivery_coordinate": (
            f"{instance.delivery_latitude},{instance.delivery_longitude}"
            if instance.delivery_latitude and instance.delivery_longitude
            else None
        ),
    }


def get_dispatcher_info(dispatcher):
    if dispatcher:
        return {
            "dispatcher_name": (
                f"{dispatcher.first_name} {dispatcher.last_name}"
                if dispatcher.first_name and dispatcher.last_name
                else None
            ),
            "dispatcher_phone": dispatcher.phone_number,
            "dispatcher_email": dispatcher.email,
        }
    return {"dispatcher_name": None, "dispatcher_phone": None, "dispatcher_email": None}
