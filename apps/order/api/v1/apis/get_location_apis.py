import requests
from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response

from apps.order.models import Order
from apps.vehicle.models import Vehicles


class GetLocationAPI(views.APIView):
    def post(self, request):
        order_id = request.data.get("order_id")
        radius = int(request.data.get("radius", 1000))

        url = "https://api.geoapify.com/v1/routematrix?apiKey=4d1a57181b7d427ebacdf105eced5c1d"
        headers = {"Content-Type": "application/json"}

        if not order_id:
            return Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, pk=order_id)
        lat_order, lon_order = order.coordinate_from.split(",")

        sources = f'"location":[{lat_order},{lon_order}]'
        targets = ""

        vehicles = Vehicles.objects.all()
        drivers = []
        for vehicle in vehicles:
            drivers.append(vehicle.driver)
            lat_driver, lon_driver = vehicle.coordinate_from.split(",")
            targets += '{"location":[' + lat_driver + "," + lon_driver + "]},"
        targets = targets[:-1]

        data = '{"mode":"drive","sources":[{' + sources + '}],"targets":[' + targets + "]}"
        resp = requests.post(url, headers=headers, data=data)

        resp_json = resp.json()
        sources_to_targets = resp_json["sources_to_targets"][0]
        available_drivers = []
        for i in range(len(sources_to_targets)):
            distance = sources_to_targets[i]["distance"]
            time = sources_to_targets[i]["time"]
            if distance <= radius:
                available_drivers.append(self.get_driver_info(drivers[i], distance, time))

        return Response(
            {"order_coordinates": order.coordinate_from, "available_drivers": available_drivers},
            status=status.HTTP_200_OK,
        )

    def get_driver_info(self, driver, distance_miles, time):
        return {
            "id": driver.id,
            "first_name": driver.first_name,
            "last_name": driver.last_name,
            "phone_number": driver.phone_number,
            "miles_out": distance_miles,
            "time": time,
            "coordinate_from": driver.vehicle.coordinate_from,
        }
