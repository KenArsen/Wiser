import re

import requests
from rest_framework.exceptions import ValidationError

from apps.order.models import Point


def _extract_zip_code(address):
    match = re.search(r"\b\d{5}(?:-\d{4})?\b", address)
    if match:
        return match.group(0)
    return None


def get_location(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"addressdetails": 1, "q": address, "format": "jsonv2", "limit": 1}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            location_data = data[0]
            zip_code = location_data["address"].get("postcode") or _extract_zip_code(
                address
            )
            return {
                "latitude": location_data["lat"],
                "longitude": location_data["lon"],
                "address": location_data["display_name"],
                "city": location_data["address"].get("city"),
                "state": location_data["address"].get("state"),
                "county": location_data["address"].get("county"),
                "zip_code": zip_code,
            }
        else:
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def create_point(order_, address, date, point_type):
    location = get_location(address=address)
    if location:
        Point.objects.create(
            order=order_,
            date=date,
            type=point_type,
            city=location["city"],
            state=location["state"],
            county=location["county"],
            address=location["address"],
            zip_code=location["zip_code"],
            latitude=location["latitude"],
            longitude=location["longitude"],
        )
    else:
        raise ValidationError({"error": f"Location not found for address: {address}"})
