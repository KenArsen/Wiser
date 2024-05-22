from django.db import models
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim

from apps.common.base_model import BaseModel


class Vehicles(BaseModel):
    class Transport(models.TextChoices):
        CARGO_VAN = "CARGO VAN", "CARGO VAN"
        SPRINTER_VAN = "SPRINTER VAN", "SPRINTER VAN"
        VAN = "VAN", "VAN"
        SPRINTER = "SPRINTER", "SPRINTER"
        BOX_TRUCK = "BOX TRUCK", "BOX TRUCK"
        SMALL_STRAIGHT = "SMALL STRAIGHT", "SMALL STRAIGHT"
        LARGE_STRAIGHT = "LARGE STRAIGHT", "LARGE STRAIGHT"
        LIFTGATE = "LIFTGATE", "LIFTGATE"
        FLATBED = "FLATBED", "FLATBED"
        TRACTOR = "TRACTOR", "TRACTOR"
        REEFER = "REEFER", "REEFER"

    # general info
    unit_id = models.CharField(max_length=255)
    transport_type = models.CharField(max_length=255, choices=Transport.choices, default=Transport.SPRINTER_VAN)
    vehicle_model = models.CharField(max_length=255, blank=True, null=True)
    vehicle_year = models.CharField(max_length=255, blank=True, null=True)
    dock_high = models.CharField(max_length=255, default="No")

    # vehicle sizes
    width = models.IntegerField(default=0, blank=True, null=True)
    height = models.IntegerField(default=0, blank=True, null=True)
    length = models.IntegerField(default=0, blank=True, null=True)
    payload = models.IntegerField(default=0, blank=True, null=True)

    # vehicle details
    vin = models.CharField(max_length=255, blank=True, null=True)
    location_to = models.CharField(max_length=255, blank=True, null=True)
    location_from = models.CharField(max_length=255, blank=True, null=True)
    location_from_date = models.DateTimeField(blank=True, null=True)
    coordinate_from = models.CharField(max_length=255, blank=True, null=True)

    # lisense info
    lisense_plate = models.CharField(max_length=255, blank=True, null=True)
    lisense_plate_state = models.CharField(max_length=255, blank=True, null=True)

    lisense_expiry_date = models.CharField(max_length=255, blank=True, null=True)
    lisense_expiry_state = models.CharField(max_length=255, blank=True, null=True)

    # owner info
    dispatcher = models.ForeignKey(
        "user.User", on_delete=models.SET_NULL, blank=True, null=True, related_name="dispatcher_vehicles"
    )
    vehicle_owner = models.ForeignKey(
        "user.User", on_delete=models.SET_NULL, blank=True, null=True, related_name="owner_vehicles"
    )
    driver = models.OneToOneField(
        "driver.Driver", on_delete=models.CASCADE, blank=True, null=True, related_name="vehicle"
    )

    def __str__(self):
        return f"ID: {self.id}, UNIT ID: {self.unit_id} - DRIVER: {self.driver}"

    def save(self, *args, **kwargs):
        if self.driver and self.driver.address:
            try:
                geolocator = Nominatim(user_agent="Wiser")
                self.location_from = self.driver.address
                location = geolocator.geocode(self.driver.address)
                if location:
                    lat, lon = location.latitude, location.longitude
                    self.coordinate_from = f"{lat},{lon}"
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                pass

        super().save(*args, **kwargs)
