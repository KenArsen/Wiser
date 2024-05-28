from geopy.distance import geodesic
from rest_framework import serializers

from apps.driver.api.v1.serializers import DriverListSerializer
from apps.driver.models import Driver
from apps.order.models import Order, Point

from .common_serializer import PointSerializer


def _get_nearby_drivers(obj, distance_=2000):
    point_1 = Point.objects.get(order=obj, type="PICK_UP")
    order_coordinate = (point_1.latitude, point_1.longitude)
    drivers = Driver.objects.all()

    nearby_drivers = []

    for driver in drivers:
        driver_coordinate = (
            driver.vehicle.location.latitude,
            driver.vehicle.location.longitude,
        )
        distance = geodesic(order_coordinate, driver_coordinate).miles

        if distance <= distance_:
            nearby_drivers.append(DriverListSerializer(driver).data)
    return nearby_drivers, len(nearby_drivers)


def _get_miles(obj):
    point_1 = Point.objects.get(order=obj, type="PICK_UP")
    point_2 = Point.objects.get(order=obj, type="DELIVER_TO")
    distance = geodesic(
        (point_1.latitude, point_1.longitude), (point_2.latitude, point_2.longitude)
    ).miles
    return int(distance)


def _get_nearby_orders(obj, radius=20):
    obj_point_1 = Point.objects.get(order=obj, type="PICK_UP")
    obj_point_2 = Point.objects.get(order=obj, type="DELIVER_TO")
    orders = Order.objects.filter(status="COMPLETED")

    nearby_orders = []

    for order in orders:
        order_point_1 = Point.objects.get(order=order, type="PICK_UP")
        order_point_2 = Point.objects.get(order=order, type="DELIVER_TO")
        distance_from = _get_miles(
            (
                obj_point_1.latitude,
                obj_point_1.longitude,
                order_point_1.latitude,
                order_point_1.longitude,
            )
        )
        distance_to = _get_miles(
            (
                obj_point_2.latitude,
                obj_point_2.longitude,
                order_point_2.latitude,
                order_point_2.longitude,
            )
        )

        if distance_from <= radius and distance_to <= radius:
            nearby_orders.append(order)
    return nearby_orders


class LoadBoardListSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "points", "created_at", "status")

        ref_name = "LoadBoardList"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        nearby_drivers, match_count = _get_nearby_drivers(instance)
        representation["match"] = match_count
        representation["miles"] = _get_miles(instance)
        return representation


class LoadBoardDetailSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

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
        representation["miles"] = _get_miles(instance)
        return representation
