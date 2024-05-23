import logging
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

geolocator = Nominatim(user_agent="Wiser")


def get_location(address):
    try:
        location = geolocator.geocode(address)
        if location is None:
            raise ValueError(f"Could not geocode address: {address}")
        return f'{location.latitude},{location.longitude}'
    except (AttributeError, GeocoderServiceError) as e:
        logging.error(f"Error geocoding address '{address}': {e}")
        return "0.000000,0.000000"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return "0.000000,0.000000"
