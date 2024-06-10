from rest_framework import serializers

from apps.driver.models import Driver
from apps.order.models import Order, Template


class NearByDriverSerializer(serializers.ModelSerializer):
    transport_type = serializers.SerializerMethodField()
    payload = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    coordinate = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ("id", "full_name", "phone_number", "transport_type", "payload", "location", "coordinate")
        ref_name = "NearByDriver"

    def get_transport_type(self, obj):
        return obj.vehicle.transport_type if getattr(obj, "vehicle", None) else None

    def get_payload(self, obj):
        return obj.vehicle.payload if getattr(obj, "vehicle", None) else None

    def get_location(self, obj):
        return obj.vehicle.location if getattr(obj, "vehicle", None) else None

    def get_coordinate(self, obj):
        return obj.vehicle.coordinate if getattr(obj, "vehicle", None) else None


class NearByOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "status", "broker", "pick_up_location", "delivery_location")
        ref_name = "NearByOrder"


class LoadBoardBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "created_at",
            "status",
            "pick_up_location",
            "pick_up_coordinate",
            "pick_up_date",
            "delivery_location",
            "delivery_coordinate",
            "delivery_date",
            "load_type",
            "broker",
            "match",
        )
        ref_name = "LoadBoardBase"


class LoadBoardListSerializer(LoadBoardBaseSerializer):
    class Meta:
        model = Order
        fields = LoadBoardBaseSerializer.Meta.fields
        ref_name = "LoadBoardList"


class LoadBoardDetailSerializer(LoadBoardBaseSerializer):
    nearby_drivers = serializers.SerializerMethodField()
    nearby_orders = serializers.SerializerMethodField()
    message_template = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = LoadBoardBaseSerializer.Meta.fields + (
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
            "match",
            "nearby_drivers",
            "nearby_orders",
            "message_template",
        )
        ref_name = "LoadBoardDetail"

    def get_nearby_drivers(self, order, distance_threshold=2000):
        # if not order.pick_up_latitude or not order.pick_up_longitude:
        #     return []
        #
        # vehicles = Vehicle.objects.filter(
        #     location_latitude__isnull=False,
        #     location_longitude__isnull=False,
        # ).only("location_latitude", "location_longitude")
        #
        # nearby_drivers = []
        # for vehicle in vehicles:
        #     distance = get_haversine_distance(
        #         order.pick_up_latitude,
        #         order.pick_up_longitude,
        #         vehicle.location_latitude,
        #         vehicle.location_longitude,
        #     )
        #
        #     if distance <= distance_threshold:
        #         nearby_drivers.append(NearByDriverSerializer(vehicle.driver).data)
        # return nearby_drivers
        return []

    def get_nearby_orders(self, order, radius=2000):
        # if not order.pick_up_latitude or not order.pick_up_longitude:
        #     return []
        #
        # orders = Order.objects.filter(
        #     status="COMPLETED",
        #     pick_up_latitude__isnull=False,
        #     pick_up_location__isnull=False,
        # ).only("pick_up_latitude", "pick_up_longitude", "delivery_latitude", "delivery_longitude")
        #
        # nearby_orders = []
        #
        # for obj in orders:
        #     distance_from = get_haversine_distance(
        #         order.pick_up_latitude,
        #         order.pick_up_longitude,
        #         obj.delivery_latitude,
        #         obj.delivery_longitude,
        #     )
        #     distance_to = get_haversine_distance(
        #         order.delivery_latitude,
        #         order.delivery_longitude,
        #         obj.delivery_latitude,
        #         obj.delivery_longitude,
        #     )
        #
        #     if distance_from <= radius and distance_to <= radius:
        #         nearby_orders.append(NearByOrderSerializer(obj).data)
        # return nearby_orders
        return []

    def get_message_template(self, _):
        template = Template.objects.filter(is_active=True).first()
        return template.content if template else None
