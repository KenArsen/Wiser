from django.db import models

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

    # vehicle sizes
    width = models.IntegerField(default=0, blank=True, null=True)
    height = models.IntegerField(default=0, blank=True, null=True)
    length = models.IntegerField(default=0, blank=True, null=True)
    payload = models.IntegerField(default=0, blank=True, null=True)

    # vehicle details
    vin = models.CharField(max_length=255, blank=True, null=True)

    # lisense info
    lisense_plate = models.CharField(max_length=255, blank=True, null=True)
    lisense_plate_state = models.CharField(max_length=255, blank=True, null=True)

    lisense_expiry_date = models.CharField(max_length=255, blank=True, null=True)
    lisense_expiry_state = models.CharField(max_length=255, blank=True, null=True)

    # owner info
    dispatcher = models.CharField(max_length=255, blank=True, null=True)
    vehicle_owner = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, blank=True, null=True, related_name="vehicles"
    )
    driver = models.ForeignKey("driver.Driver", on_delete=models.CASCADE, related_name="vehicles")

    def __str__(self):
        return f"ID: {self.unit_id} - DRIVER: {self.driver}"
