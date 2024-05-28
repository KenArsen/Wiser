from django.db import models

from apps.common.enums import TransportType
from apps.common.models import BaseModel


class Vehicle(BaseModel):
    # general info
    unit_id = models.CharField(max_length=255)
    transport_type = models.CharField(
        max_length=255,
        choices=TransportType.choices,
        default=TransportType.SPRINTER_VAN,
    )
    vehicle_model = models.CharField(max_length=255, blank=True, null=True)
    vehicle_year = models.CharField(max_length=4, blank=True, null=True)

    # vehicle sizes
    width = models.SmallIntegerField(blank=True, null=True)
    height = models.SmallIntegerField(blank=True, null=True)
    length = models.SmallIntegerField(blank=True, null=True)
    payload = models.SmallIntegerField(blank=True, null=True)

    # vehicle details
    vin = models.CharField(max_length=255, blank=True, null=True)

    # lisense info
    lisense_plate = models.CharField(max_length=255, blank=True, null=True)
    lisense_state = models.CharField(max_length=255, blank=True, null=True)
    lisense_expiry_date = models.DateTimeField(blank=True, null=True)
    insurance_expiry_date = models.DateTimeField(blank=True, null=True)

    # owner info
    dispatcher = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dispatchers",
    )
    owner = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="owners",
    )
    driver = models.OneToOneField(
        "driver.Driver",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="vehicle",
    )

    def __str__(self):
        return f"{self.unit_id}"


class Location(BaseModel):
    vehicle = models.OneToOneField(
        Vehicle, on_delete=models.CASCADE, related_name="location"
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.address
