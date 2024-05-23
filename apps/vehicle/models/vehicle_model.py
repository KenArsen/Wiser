from django.db import models
from apps.common.base_model import BaseModel
from apps.common.nominatim import get_location


class Vehicles(BaseModel):
    class Transport(models.TextChoices):
        CARGO_VAN = "CARGO VAN", "Cargo Van"
        SPRINTER_VAN = "SPRINTER VAN", "Sprinter Van"
        VAN = "VAN", "Van"
        SPRINTER = "SPRINTER", "Sprinter"
        BOX_TRUCK = "BOX TRUCK", "Box Truck"
        SMALL_STRAIGHT = "SMALL STRAIGHT", "Small Straight"
        LARGE_STRAIGHT = "LARGE STRAIGHT", "Large Straight"
        LIFTGATE = "LIFTGATE", "Liftgate"
        FLATBED = "FLATBED", "Flatbed"
        TRACTOR = "TRACTOR", "Tractor"
        REEFER = "REEFER", "Reefer"

    # general info
    unit_id = models.CharField(max_length=255)
    transport_type = models.CharField(max_length=255, choices=Transport.choices, default=Transport.SPRINTER_VAN)
    vehicle_model = models.CharField(max_length=255, blank=True, null=True)
    vehicle_year = models.CharField(max_length=255, blank=True, null=True)
    dock_high = models.CharField(max_length=255, default="No")

    # vehicle sizes
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    payload = models.IntegerField(blank=True, null=True)

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

    # def save(self, *args, **kwargs):
    #     if self.driver and self.driver.address:
    #         self.location_from = self.driver.address
    #         location = get_location(address=self.driver.address)
    #         if location:
    #             self.coordinate_from = location
    #     super().save(*args, **kwargs)
