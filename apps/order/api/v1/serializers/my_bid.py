from rest_framework import serializers

from apps.order.models import Order


class MiBidBaseSerializer(serializers.ModelSerializer):
    dispatcher_name = serializers.SerializerMethodField()
    dispatcher_phone = serializers.SerializerMethodField()
    dispatcher_email = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "created_at",
            "status",
            "broker",
            "pick_up_location",
            "pick_up_coordinate",
            "pick_up_date",
            "delivery_location",
            "delivery_coordinate",
            "delivery_date",
            "dispatcher_name",
            "dispatcher_email",
            "dispatcher_phone",
        )
        ref_name = "MyBidBase"

    def get_dispatcher_name(self, instance):
        return instance.user.full_name

    def get_dispatcher_email(self, instance):
        return instance.user.email

    def get_dispatcher_phone(self, instance):
        return instance.user.phone_number


class MyBidListSerializer(MiBidBaseSerializer):
    broker_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = MiBidBaseSerializer.Meta.fields + ("broker_price",)
        ref_name = "MyBidList"

    def get_broker_price(self, instance):
        return instance.letter.broker_price if getattr(instance, "letter", None) else None


class MyBidHistorySerializer(MiBidBaseSerializer):
    broker_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = MiBidBaseSerializer.Meta.fields + ("broker_price",)
        ref_name = "MyBidHistory"

    def get_broker_price(self, instance):
        return instance.letter.broker_price if getattr(instance, "letter", None) else None


class MyBidDetailSerializer(MiBidBaseSerializer):
    broker_price = serializers.SerializerMethodField()
    driver_price = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = MiBidBaseSerializer.Meta.fields + (
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
            "message",
        )
        ref_name = "MyBidDetail"

    def get_broker_price(self, instance):
        return instance.letter.broker_price if getattr(instance, "letter", None) else None

    def get_driver_price(self, instance):
        return instance.letter.driver_price if getattr(instance, "letter", None) else None

    def get_message(self, instance):
        return instance.letter.comment if getattr(instance, "letter", None) else None
