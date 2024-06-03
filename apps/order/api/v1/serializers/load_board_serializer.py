from rest_framework import serializers

from apps.common.locations import get_haversine_distance
from apps.driver.models import Driver
from apps.order.models import Order, Template
from apps.vehicle.models import Vehicle


class NearByDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("id", "last_name", "first_name", "phone_number")
        ref_name = "NearByDriver"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        vehicle = getattr(instance, "vehicle", None)

        vehicle_info = get_vehicle_info(vehicle)
        representation.update(vehicle_info)

        return representation


class NearByOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "status", "broker", "pick_up_location", "delivery_location")
        ref_name = "NearByOrder"


class LoadBoardBaseSerializer(serializers.ModelSerializer):
    pick_up_coordinate = serializers.SerializerMethodField()
    delivery_coordinate = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
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
        ref_name = 'LoadBoardBase'

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        _update_match(instance)
        return representation


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
            "match",
            "nearby_drivers",
            "nearby_orders",
            "message_template",
        )
        ref_name = "LoadBoardDetail"

    def get_nearby_drivers(self, order, distance_threshold=2000):
        if not order.pick_up_latitude or not order.pick_up_longitude:
            return []

        vehicles = Vehicle.objects.filter(
            location_latitude__isnull=False,
            location_longitude__isnull=False,
        ).only("location_latitude", "location_longitude")

        nearby_drivers = []
        for vehicle in vehicles:
            distance = get_haversine_distance(
                order.pick_up_latitude,
                order.pick_up_longitude,
                vehicle.location_latitude,
                vehicle.location_longitude,
            )

            if distance <= distance_threshold:
                nearby_drivers.append(NearByDriverSerializer(vehicle.driver).data)

        return nearby_drivers

    def get_nearby_orders(self, order, radius=2000):
        if not order.pick_up_latitude or not order.pick_up_longitude:
            return []

        orders = Order.objects.filter(
            status="COMPLETED",
            pick_up_latitude__isnull=False,
            pick_up_location__isnull=False,
        ).only("pick_up_latitude", "pick_up_longitude", "delivery_latitude", "delivery_longitude")

        nearby_orders = []

        for obj in orders:
            distance_from = get_haversine_distance(
                order.pick_up_latitude,
                order.pick_up_longitude,
                obj.delivery_latitude,
                obj.delivery_longitude,
            )
            distance_to = get_haversine_distance(
                order.delivery_latitude,
                order.delivery_longitude,
                obj.delivery_latitude,
                obj.delivery_longitude,
            )

            if distance_from <= radius and distance_to <= radius:
                nearby_orders.append(NearByOrderSerializer(obj).data)
        return nearby_orders

    def get_message_template(self, instance):
        template = Template.objects.filter(is_active=True).first()
        return template.content if template else None


def get_vehicle_info(vehicle):
    if vehicle:
        return {
            "transport_type": vehicle.transport_type,
            "payload": vehicle.payload,
            "location": vehicle.location,
            "coordinates": (
                f"{vehicle.location_latitude},{vehicle.location_longitude}"
                if vehicle.location_latitude and vehicle.location_longitude
                else None
            ),
        }
    else:
        return {
            "transport_type": None,
            "payload": None,
            "location": None,
            "coordinates": None,
        }


def _update_match(order, distance_threshold=2000):
    if not order.pick_up_latitude or not order.pick_up_longitude:
        return

    vehicles = Vehicle.objects.filter(
        location_latitude__isnull=False,
        location_longitude__isnull=False,
    ).only("location_latitude", "location_longitude")
    match = sum(
        1
        for vehicle in vehicles
        if get_haversine_distance(
            order.pick_up_latitude, order.pick_up_longitude, vehicle.location_latitude, vehicle.location_longitude
        )
        <= distance_threshold
    )

    order.match = match
    order.save(update_fields=["match"])
