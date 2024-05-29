from geopy.distance import geodesic
from rest_framework import serializers

from apps.driver.models import Driver
from apps.order.models import Order
from apps.vehicle.models import Vehicle


class NearByDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("id", "last_name", "first_name")
        ref_name = "NearByDriver"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        vehicle = getattr(instance, "vehicle", None)
        if vehicle:
            representation["transport_type"] = vehicle.transport_type
            representation["location"] = vehicle.location
        return representation


def _get_nearby_drivers(order, distance_threshold=2000):
    order_coordinates = (order.pick_up_latitude, order.pick_up_longitude)
    vehicles = Vehicle.objects.all()

    nearby_drivers = []

    for vehicle in vehicles:
        driver_coordinates = (vehicle.location_latitude, vehicle.location_longitude)
        distance = geodesic(order_coordinates, driver_coordinates).miles

        if distance <= distance_threshold:
            nearby_drivers.append(NearByDriverSerializer(vehicle.driver).data)

    return nearby_drivers, len(nearby_drivers)


def _get_nearby_orders(obj, radius=20):
    orders = Order.objects.filter(status="COMPLETED")

    nearby_orders = []

    for order in orders:
        distance_from = geodesic(
            (obj.pick_up_latitude, obj.pick_up_longitude),
            (order.pick_up_latitude, order.pick_up_longitude),
        ).miles
        distance_to = geodesic(
            (obj.delivery_latitude, obj.delivery_longitude),
            (order.delivery_latitude, order.delivery_longitude),
        ).miles

        if distance_from <= radius and distance_to <= radius:
            nearby_orders.append(order)
    return nearby_orders


class LoadBoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "status",
            "pick_up_location",
            "delivery_location",
            "load_type",
            "broker",
        )

        ref_name = "LoadBoardList"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        nearby_drivers, match_count = _get_nearby_drivers(instance)
        representation["match"] = match_count
        return representation


class LoadBoardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "LoadBoardDetail"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        nearby_drivers, match_count = _get_nearby_drivers(instance)
        representation["nearby_drivers"] = nearby_drivers
        representation["nearby_orders"] = _get_nearby_orders(instance)
        representation["match"] = match_count
        return representation
