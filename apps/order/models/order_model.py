import logging

from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.common.enums import OrderStatus, PointType, SubStatus
from apps.common.models import BaseModel


class Order(BaseModel):
    user = models.ForeignKey(
        "user.User", on_delete=models.SET_NULL, null=True, blank=True
    )

    status = models.CharField(
        max_length=100, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )

    order_number = models.CharField(max_length=255, blank=True, null=True)

    transit_time = models.PositiveIntegerField(blank=True, null=True)
    transit_distance = models.PositiveIntegerField(blank=True, null=True)

    line = models.CharField(max_length=255, blank=True, null=True)

    broker = models.CharField(max_length=255, blank=True, null=True)
    broker_phone = models.CharField(max_length=255, blank=True, null=True)
    broker_email = models.EmailField(null=True, blank=True)
    posted = models.DateTimeField(blank=True, null=True, default=timezone.now)
    expires = models.DateTimeField(blank=True, null=True, default=timezone.now)
    dock_level = models.CharField(max_length=255, blank=True, null=True)
    hazmat = models.CharField(max_length=255, blank=True, null=True)
    fast_load = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=400, blank=True, null=True)

    load_type = models.CharField(max_length=255, blank=True, null=True)
    vehicle_required = models.CharField(max_length=255, blank=True, null=True)
    pieces = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    dimensions = models.CharField(max_length=255, blank=True, null=True)
    stackable = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.broker_email

    def clean(self):
        if self.expires is None:
            raise ValidationError(
                {"error": f"This {self.order_number} does not expire!"}
            )

        if (
            self.expires <= timezone.localtime(timezone.now())
            and self.status == "PENDING"
        ):
            raise ValidationError(
                {"error": f"This {self.order_number} order has already expired!"}
            )

    def move_to_history(self):
        if self.user is not None:
            self.status = "EXPIRED"
            self.save()
            logging.info(f"------ Order {self.id} moved to history --------")
        else:
            logging.info(f"------ Order {self.id} deleted --------")
            self.delete()


class Point(BaseModel):
    order = models.ForeignKey(
        "order.Order", on_delete=models.CASCADE, related_name="points"
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    type = models.CharField(
        max_length=255, choices=PointType.choices, default=PointType.PICK_UP
    )

    def __str__(self):
        return f"{self.address}"


class Assign(BaseModel):
    order = models.OneToOneField(
        "order.Order", on_delete=models.CASCADE, related_name="assign"
    )
    broker_company = models.CharField(max_length=255)
    rate_confirmation = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.broker_company}"


class MyLoadStatus(BaseModel):
    previous_status = models.PositiveSmallIntegerField(
        choices=SubStatus.choices, null=True
    )
    current_status = models.PositiveSmallIntegerField(
        choices=SubStatus.choices, null=True
    )
    next_status = models.PositiveSmallIntegerField(choices=SubStatus.choices, null=True)
    order = models.OneToOneField(
        "order.Order",
        on_delete=models.CASCADE,
        related_name="my_load_status",
    )

    def __str__(self):
        return f"{self.order}"


class File(BaseModel):
    order = models.ForeignKey(
        "order.Order", on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(upload_to="order_files/%Y/%m/%d")

    def __str__(self):
        return f"{self.order}"
