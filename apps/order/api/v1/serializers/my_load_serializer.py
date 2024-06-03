from rest_framework import serializers

from apps.order.models import Order

from .common_serializer import MyLoadStatusSerializer


class MyLoadBaseSerializer(serializers.ModelSerializer):
    my_load_status = MyLoadStatusSerializer(many=False, read_only=True)
    pick_up_coordinate = serializers.SerializerMethodField()
    delivery_coordinate = serializers.SerializerMethodField()
    dispatcher_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "created_at",
            "updated_at",
            "status",
            "my_load_status",
            "broker",
            "pick_up_location",
            "pick_up_coordinate",
            "pick_up_date",
            "delivery_location",
            "delivery_coordinate",
            "delivery_date",
            "dispatcher_name",
        )
        ref_name = "MyLoadBase"

    def get_pick_up_coordinate(self, instance):
        return (
            f"{instance.pick_up_latitude},{instance.pick_up_longitude}"
            if instance.pick_up_latitude and instance.pick_up_longitude
            else None
        )

    def get_delivery_coordinate(self, instance):
        return (
            f"{instance.delivery_latitude},{instance.delivery_longitude}"
            if instance.delivery_latitude and instance.delivery_longitude
            else None
        )

    def get_dispatcher_name(self, instance):
        return (
            f"{instance.user.first_name} {instance.user.last_name}"
            if instance.user.first_name and instance.user.last_name
            else None
        )


class MyLoadListSerializer(MyLoadBaseSerializer):
    class Meta:
        model = Order
        fields = MyLoadBaseSerializer.Meta.fields
        ref_name = "MyLoadList"


class MyLoadDetailSerializer(MyLoadBaseSerializer):
    broker_price = serializers.SerializerMethodField()
    driver_price = serializers.SerializerMethodField()
    driver_name = serializers.SerializerMethodField()
    driver_email = serializers.SerializerMethodField()
    driver_phone = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = MyLoadBaseSerializer.Meta.fields + (
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
            "broker_price",
            "driver_price",
            "driver_name",
            "driver_email",
            "driver_phone",
        )
        ref_name = "MyLoadDetail"

    def get_broker_price(self, instance):
        return instance.letter.broker_price if getattr(instance, "letter", None) else None

    def get_driver_price(self, instance):
        return instance.letter.driver_price if getattr(instance, "letter", None) else None

    def get_driver_name(self, instance):
        return (
            f"{instance.letter.driver.first_name} {instance.letter.driver.last_name}"
            if instance.letter.driver.first_name and instance.letter.driver.last_name
            else None
        )

    def get_driver_email(self, instance):
        return instance.letter.driver.email if getattr(instance, "letter", None) else None

    def get_driver_phone(self, instance):
        return instance.letter.driver.phone_number if getattr(instance, "letter", None) else None
