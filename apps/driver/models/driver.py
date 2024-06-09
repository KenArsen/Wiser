from django.db import models

from apps.common.image import ImageService
from apps.common.models import BaseModel


class Driver(BaseModel, ImageService):
    # driver info
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)

    ssn = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    second_driver = models.BooleanField(default=False)

    # driver license
    license_number = models.CharField(max_length=255, blank=True, null=True)
    license_state = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}" if self.last_name and self.first_name else None

    def get_license_info(self):
        return f"{self.license_number} ({self.license_state})" if self.license_state and self.license_state else None
