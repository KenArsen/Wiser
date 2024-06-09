import logging

from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.common.enums import OrderStatus, SubStatus
from apps.common.locations import get_location
from apps.common.models import BaseModel
from apps.user.models import User


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=100, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    order_number = models.CharField(max_length=255, blank=True, null=True)

    pick_up_location = models.CharField(max_length=255, blank=True, null=True)
    pick_up_latitude = models.FloatField(blank=True, null=True)
    pick_up_longitude = models.FloatField(blank=True, null=True)
    pick_up_date = models.DateTimeField(blank=True, null=True)

    delivery_location = models.CharField(max_length=255, blank=True, null=True)
    delivery_latitude = models.FloatField(blank=True, null=True)
    delivery_longitude = models.FloatField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)

    stops = models.CharField(max_length=255, blank=True, null=True)
    broker = models.CharField(max_length=255, blank=True, null=True)
    broker_phone = models.CharField(max_length=255, blank=True, null=True)
    broker_email = models.EmailField(null=True, blank=True)
    posted = models.DateTimeField(blank=True, null=True)
    expires = models.DateTimeField(default=timezone.now)
    dock_level = models.BooleanField(default=False)
    hazmat = models.BooleanField(default=False)
    amount = models.CharField(max_length=255, blank=True, null=True)
    fast_load = models.BooleanField(default=False)
    notes = models.TextField(max_length=400, blank=True, null=True)
    load_type = models.CharField(max_length=255, blank=True, null=True)
    vehicle_required = models.CharField(max_length=255, blank=True, null=True)
    pieces = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    dimensions = models.CharField(max_length=255, blank=True, null=True)
    stackable = models.BooleanField(default=False)

    match = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.broker_email

    def save(self, *args, **kwargs):
        if self.pick_up_location:
            pick_up_location = get_location(self.pick_up_location)
            if pick_up_location:
                self.pick_up_latitude = pick_up_location.latitude
                self.pick_up_longitude = pick_up_location.longitude

        if self.delivery_location:
            delivery_location = get_location(self.delivery_location)
            if delivery_location:
                self.delivery_latitude = delivery_location.latitude
                self.delivery_longitude = delivery_location.longitude

        super().save(*args, **kwargs)

    def clean(self):
        if self.expires <= timezone.localtime(timezone.now()) and self.status == OrderStatus.PENDING:
            raise ValidationError({"error": f"This {self.order_number} order has already expired!"})

    def move_to_history(self):
        if self.user is not None:
            self.status = OrderStatus.EXPIRED
            self.save()
            logging.info(f"------ Order {self.id} moved to history --------")
        else:
            logging.info(f"------ Order {self.id} deleted --------")
            self.delete()

    @property
    def pick_up_coordinate(self):
        return (
            f"{self.pick_up_latitude},{self.pick_up_longitude}"
            if self.pick_up_latitude and self.pick_up_longitude
            else None
        )

    @property
    def delivery_coordinate(self):
        return (
            f"{self.delivery_latitude},{self.delivery_longitude}"
            if self.delivery_latitude and self.delivery_longitude
            else None
        )


class Assign(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="assign")
    broker_company = models.CharField(max_length=255)
    rate_confirmation = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.broker_company}"


class MyLoadStatus(BaseModel):
    previous_status = models.PositiveSmallIntegerField(choices=SubStatus.choices, null=True)
    current_status = models.PositiveSmallIntegerField(choices=SubStatus.choices, null=True)
    next_status = models.PositiveSmallIntegerField(choices=SubStatus.choices, null=True)
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="my_load_status",
    )

    def __str__(self):
        return f"{self.order}"


class File(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="order_files/%Y/%m/%d")

    def __str__(self):
        return f"{self.order}"
