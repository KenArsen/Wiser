from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema

from api.utils.decorators_swagger import filtered_drivers_response, time_until_delivery_response, order_data_spec
from apps.read_email.models import Order
from api.serializers.read_email import OrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable


from rest_framework.permissions import IsAuthenticated
from api.utils.permissions import IsDispatcher, IsAdmin
from apps.user.models import User


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.filter(is_active=True)
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher,)

    @swagger_auto_schema(
        responses=time_until_delivery_response,
        operation_summary="Get time_until_delivery"
    )
    def get_delivery_time(self, request, pk=None):
        order = self.get_object()

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

    @swagger_auto_schema(
        responses=filtered_drivers_response,
        operation_summary="Get location order details"
    )
    def get_location_order(self, request, pk=None):
        order = self.get_object()
        pick_up_at = order.pick_up_at if order.is_active else None

        if not pick_up_at:
            return Response({"error": "pick_up_at not specified for the order."}, status=400)

        try:
            geolocator = Nominatim(user_agent='user')
            location = geolocator.geocode(pick_up_at, timeout=10)

            if not location:
                return Response({"error": "Failed to geocode pick_up_at location."}, status=400)

            lat_order, lon_order = location.latitude, location.longitude

            active_drivers = User.objects.filter(is_active=True, roles__name='DRIVER', lat__isnull=False,
                                                 lon__isnull=False)

            filtered_drivers = []
            for driver in active_drivers:
                lat_driver, lon_driver = driver.lat, driver.lon

                distance_km = geodesic((lat_order, lon_order), (lat_driver, lon_driver)).kilometers

                if distance_km <= 100:

                    filtered_drivers.append({
                        "id": driver.id,
                        "first_name": driver.first_name,
                        "vehicle_type": driver.vehicle_type,
                        "phone_number": driver.phone_number,
                        "MILES OUT": distance_km,
                        "lat": driver.lat,
                        "lon": driver.lon
                    })

            return Response({"available_drivers": filtered_drivers})

        except GeocoderTimedOut:
            return Response({"error": "Geocoding timed out."}, status=500)
        except GeocoderUnavailable:
            return Response({"error": "Geocoding service is unavailable."}, status=500)
        except Exception as e:
            return Response({"error": f"An error occurred during geocoding: {str(e)}"}, status=500)


class OrderFilterView(APIView):

    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher,)

    @swagger_auto_schema(**order_data_spec)
    def get(self, request):
        pick_up_at = request.query_params.get('pick_up_at')
        deliver_to = request.query_params.get('deliver_to')
        miles = request.query_params.get('miles')

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
