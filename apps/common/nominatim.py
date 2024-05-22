from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Wiser")


def get_location(address):
    location = geolocator.geocode(address)
    return f'{location.latitude},{location.longitude}'
