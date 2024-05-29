from geopy.geocoders import Nominatim


def get_location(address):
    geolocator = Nominatim(user_agent="Wiser")
    location = geolocator.geocode(address)
    return location
