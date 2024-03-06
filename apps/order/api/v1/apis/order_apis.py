from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.decorators_swagger import (
    filtered_drivers_response,
    time_until_delivery_response,
)
from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers.order_serializer import OrderSerializer
from apps.order.models import Order
from apps.user.models import User


class OrderListAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        tags=["Order"],
        operation_summary="List orders",
        operation_description="Get a list of active orders with default status",
    )
    def get(self, request):
        orders = Order.objects.filter(is_active=True, order_status="DEFAULT")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        tags=["Order"],
        operation_summary="Create order",
        operation_description="Create a new order",
        request_body=OrderSerializer,
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        tags=["Order"],
        operation_summary="Retrieve order details",
        operation_description="Retrieve details of a specific order",
    )
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=True, order_status="DEFAULT")
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderUpdateAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        tags=["Order"],
        operation_summary="Update order",
        operation_description="Update details of a specific order",
        request_body=OrderSerializer,
    )
    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=True, order_status="DEFAULT")
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["Order"],
        operation_description="Update an existing order partially",
        request_body=OrderSerializer,
        responses={200: OrderSerializer()},
    )
    def patch(self, request, pk=None):
        order = Order.objects.filter(is_active=True, order_status="DEFAULT", pk=pk).first()
        if not order:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDeleteAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        tags=["Order"],
        operation_summary="Delete order",
        operation_description="Delete a specific order",
    )
    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=True, order_status="DEFAULT")
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetDeliveryTime(views.APIView):
    @swagger_auto_schema(
        tags=["Order"], responses=time_until_delivery_response, operation_summary="Get time_until_delivery"
    )
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        delivery_time = order.deliver_date_EST if order.is_active else None
        if delivery_time is None:
            return Response({"error": "Delivery time not specified or order is not active."}, status=400)
        current_time = timezone.localtime(timezone.now())
        time_until_delivery = delivery_time - current_time
        total_seconds = time_until_delivery.total_seconds()
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)
        hours += days * 24
        time_until_delivery_readable = f"{int(hours)}:{int(minutes)}"
        return Response({"TIME LEFT TO DELIVER": time_until_delivery_readable})


class GetLocationOrder(views.APIView):
    @swagger_auto_schema(
        tags=["Order"], responses=filtered_drivers_response, operation_summary="Get location order details"
    )
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        pick_up_at = order.pick_up_at if order.is_active else None
        if not pick_up_at:
            return Response({"error": "pick_up_at not specified for the order."}, status=400)
        try:
            geolocator = Nominatim(user_agent="user")
            location = geolocator.geocode(pick_up_at, timeout=10)
            if not location:
                return Response({"error": "Failed to geocode pick_up_at location."}, status=400)
            lat_order, lon_order = location.latitude, location.longitude
            distance_km = 0
            if request.method == "GET":
                active_drivers = User.objects.filter(
                    is_active=True, roles__name="DRIVER", lat__isnull=False, lon__isnull=False
                )
                selected_driver_id = request.query_params.get("selected_driver_id")
                filtered_drivers = []
                for driver in active_drivers:
                    lat_driver, lon_driver = driver.lat, driver.lon
                    distance_km = geodesic((lat_order, lon_order), (lat_driver, lon_driver)).kilometers
                    if distance_km <= 100:
                        estimated_speed_kmph = 50
                        estimated_time_hours = distance_km / estimated_speed_kmph
                        transit_time = round(estimated_time_hours * 60, 1)
                        driver_data = {
                            "id": driver.id,
                            "first_name": driver.first_name,
                            "vehicle_type": driver.vehicle_type,
                            "phone_number": driver.phone_number,
                            "MILES OUT": round(distance_km, 1),
                            "TRANSIT TIME": transit_time,
                            "lat": driver.lat,
                            "lon": driver.lon,
                        }
                        filtered_drivers.append(driver_data)
                        if selected_driver_id and int(selected_driver_id) == driver.id:
                            return Response(driver_data)
                return Response({"available_drivers": filtered_drivers})
            elif request.method == "POST":
                selected_driver_id = request.data.get("selected_driver_id")
                if selected_driver_id:
                    selected_driver = get_object_or_404(
                        User, id=selected_driver_id, is_active=True, roles__name="DRIVER"
                    )
                    order.user = selected_driver
                    order.save()
                    lat_order, lon_order = location.latitude, location.longitude
                    lat_driver, lon_driver = selected_driver.lat, selected_driver.lon
                    distance_km = geodesic((lat_order, lon_order), (lat_driver, lon_driver)).kilometers
                    estimated_speed_kmph = 50
                    estimated_time_hours = distance_km / estimated_speed_kmph
                    transit_time = round(estimated_time_hours * 60, 1)
                    driver_info = {
                        "id": selected_driver.id,
                        "first_name": selected_driver.first_name,
                        "vehicle_type": selected_driver.vehicle_type,
                        "phone_number": selected_driver.phone_number,
                        "MILES OUT": round(distance_km, 1),
                        "TRANSIT TIME": transit_time,
                        "lat": selected_driver.lat,
                        "lon": selected_driver.lon,
                    }
                    return Response({"message": "Driver assigned successfully.", "selected_driver_info": driver_info})
                else:
                    return Response({"error": "selected_driver_id not provided in the request data."}, status=400)
        except GeocoderTimedOut:
            return Response({"error": "Geocoding timed out."}, status=500)
        except GeocoderUnavailable:
            return Response({"error": "Geocoding service is unavailable."}, status=500)
        except Exception as e:
            return Response({"error": f"An error occurred during geocoding: {str(e)}"}, status=500)


class OrderFilterView(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        tags=["Order"],
        operation_summary="Filter orders",
        operation_description="Filter orders based on pick up location, delivery location, and miles.",
    )
    def get(self, request):
        pick_up_at = request.query_params.get("pick_up_at")
        deliver_to = request.query_params.get("deliver_to")
        miles = request.query_params.get("miles")
        filtered_orders = Order.objects.filter(is_active=True)
        filter_conditions = Q()
        if pick_up_at:
            filter_conditions |= Q(pick_up_at__icontains=pick_up_at)
        if deliver_to:
            filter_conditions |= Q(deliver_to__icontains=deliver_to)
        if miles:
            filter_conditions |= Q(miles__exact=miles)
        if filter_conditions:
            filtered_orders = filtered_orders.filter(filter_conditions)
        serialized_data = OrderSerializer(filtered_orders, many=True)
        return Response(serialized_data.data)
