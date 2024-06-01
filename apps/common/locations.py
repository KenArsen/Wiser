from math import atan2, cos, radians, sin, sqrt

from geopy.geocoders import Nominatim


def get_location(address):
    geolocator = Nominatim(user_agent="Wiser")
    location = geolocator.geocode(address)
    return location


def get_haversine_distance(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    miles = 3956 * c  # Radius of Earth in miles
    return miles
