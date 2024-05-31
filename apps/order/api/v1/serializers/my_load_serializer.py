from rest_framework import serializers

from apps.order.models import Order

from .common_serializer import MyLoadStatusSerializer


class MyLoadListSerializer(serializers.ModelSerializer):
    my_load_status = MyLoadStatusSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "updated_at",
            "status",
            "my_load_status",
            "broker",
            "pick_up_location",
            "delivery_location",
        )
        ref_name = "MyLoadList"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        dispatcher = instance.user

        dispatcher_info = get_dispatcher_info(dispatcher)
        representation.update(dispatcher_info)

        return representation


class MyLoadDetailSerializer(serializers.ModelSerializer):
    my_load_status = MyLoadStatusSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = (
            "created_at",
            "updated_at",
            "status",
            "my_load_status",
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
        ref_name = "MyLoadDetail"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        letter = getattr(instance, "letter", None)
        driver = getattr(letter, "driver", None) if letter else None

        letter_info = get_letter_info(letter)
        representation.update(letter_info)

        driver_info = get_driver_info(driver)
        representation.update(driver_info)

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
        }
    return {"dispatcher_name": None}


def get_driver_info(driver):
    if driver:
        return {
            "driver_name": (
                f"{driver.first_name} {driver.last_name}" if driver.first_name and driver.last_name else None
            ),
            "driver_phone": driver.phone_number,
            "driver_email": driver.email,
        }
    else:
        return {"driver_name": None, "driver_phone": None, "driver_email": None}


def get_letter_info(letter):
    if letter:
        return {
            "broker_price": letter.broker_price,
            "driver_price": letter.driver_price,
        }
    else:
        return {"broker_price": None, "driver_price": None}
