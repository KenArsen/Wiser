import logging

import requests
from celery import shared_task

from ..vehicle.models import Vehicles
from .models import Order


@shared_task
def get_location():
    logging.info(f'{"#" * 10} Getting location start {"#" * 10}')
    orders = Order.objects.all()
    for order in orders:
        lat_order, lon_order = order.coordinate_from.split(",")

        vehicles = Vehicles.objects.all()
        match = 0
        for vehicle in vehicles:
            lat_driver, lon_driver = vehicle.coordinate_from.split(",")
            distance_miles = get_distance_and_time(lon_order, lat_order, lon_driver, lat_driver)
            if distance_miles <= 1000:
                match += 1

        order.match = match
        order.save()
    logging.info(f'{"#" * 10} Getting location end {"#" * 10}')


def get_distance_and_time(lon_order, lat_order, lon_driver, lat_driver):
    url = (
        f"https://routing.openstreetmap.de/routed-car/route/v1/driving/"
        f"{lon_order},{lat_order};{lon_driver},{lat_driver}?overview=false&geometries=polyline&steps=true"
    )
    response = requests.get(url)
    data = response.json()
    distance_miles = data.get("routes")[0]["distance"] / 1000 * 0.62137119
    return distance_miles
