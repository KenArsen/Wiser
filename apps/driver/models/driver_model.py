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
    lisense_number = models.CharField(max_length=255, blank=True, null=True)
    lisense_state = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    # driver status
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email}"
