from rest_framework import serializers

from apps.order.models import Order

from .common import MyLoadStatusSerializer


class MyLoadBaseSerializer(serializers.ModelSerializer):
    my_load_status = MyLoadStatusSerializer(many=False, read_only=True)
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

    def get_dispatcher_name(self, instance):
        return instance.user.full_name


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
            "posted_date",
            "expires_date",
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
        return instance.letter.driver.full_name

    def get_driver_email(self, instance):
        return instance.letter.driver.email if getattr(instance, "letter", None) else None

    def get_driver_phone(self, instance):
        return instance.letter.driver.phone_number if getattr(instance, "letter", None) else None
