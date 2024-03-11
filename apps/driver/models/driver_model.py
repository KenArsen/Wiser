from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.base_model import BaseModel
from apps.common.image import ImageService


class Driver(BaseModel, ImageService):
    # driver info
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="First Name")
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Last Name")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    ssn = models.CharField(max_length=255, blank=True, null=True, verbose_name="SSN")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name="City")
    state = models.CharField(max_length=255, blank=True, null=True, verbose_name="State")
    zip_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Zip")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Emergency Phone")
    second_driver = models.BooleanField(default=False, verbose_name="Second Driver (team)")

    # driver license
    lisense_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lisense Number")
    lisense_state = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lisense State")
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Type")
    expiration_date = models.DateField(blank=True, null=True, verbose_name="Expiration Date")

    # driver status
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
