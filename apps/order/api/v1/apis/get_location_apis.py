import requests
from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response

from apps.driver.models import Driver
from apps.order.models import Order
from apps.vehicle.models import Vehicles


class GetLocationAPI(views.APIView):
    def post(self, request):
        order_id = request.data.get("order_id")
        driver_id = request.data.get("driver_id")
        radius = int(request.data.get("radius", 100))

        if not order_id:
            return Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, pk=order_id)
        lat_order, lon_order = order.coordinate_from.split(",")

        if driver_id:
            driver = get_object_or_404(Driver, id=driver_id)
            vehicle = driver.vehicle
            lat_driver, lon_driver = vehicle.coordinate_from.split(",")
            distance_km, time = self.get_distance_and_time(lon_order, lat_order, lon_driver, lat_driver)
            driver_info = self.get_driver_info(driver, distance_km, time)
            return Response(
                {"message": "Driver assigned successfully.", "selected_driver_info": driver_info},
                status=status.HTTP_200_OK,
            )

        drivers = []
        vehicles = Vehicles.objects.all()
        for vehicle in vehicles:
            lat_driver, lon_driver = vehicle.coordinate_from.split(",")
            distance_miles, time = self.get_distance_and_time(lon_order, lat_order, lon_driver, lat_driver)
            if distance_miles <= radius:
                driver = Driver.objects.get(email=vehicle.driver)
                driver_info = self.get_driver_info(driver, distance_miles, time)
                drivers.append(driver_info)

        return Response(
            {"order_coordinates": order.coordinate_from, "available_drivers": drivers}, status=status.HTTP_200_OK
        )

    def get_distance_and_time(self, lon_order, lat_order, lon_driver, lat_driver):
        url = (
            f"https://routing.openstreetmap.de/routed-car/route/v1/driving/"
            f"{lon_order},{lat_order};{lon_driver},{lat_driver}?overview=false&geometries=polyline&steps=true"
        )
        response = requests.get(url)
        data = response.json()
        distance_miles = data.get("routes")[0]["distance"] / 1000 * 0.62137119
        time = distance_miles / 55.0
        return distance_miles, time

    def get_driver_info(self, driver, distance_miles, time):
        return {
            "id": driver.id,
            "first_name": driver.first_name,
            "last_name": driver.last_name,
            "phone_number": driver.phone_number,
            "miles_out": round(distance_miles, 1),
            "time": round(time, 2),
            "coordinate_from": driver.vehicle.coordinate_from,
        }
