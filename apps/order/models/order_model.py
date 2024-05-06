import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.common.base_model import BaseModel


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        AWAITING_BID = "AWAITING_BID", "AWAITING BID"
        REFUSED = "REFUSED", "REFUSED"
        ASSIGN = "ASSIGN", "ASSIGN"
        CHECKOUT = "CHECKOUT", "CHECKOUT"
        COMPLETED = "COMPLETED", "COMPLETED"
        CANCELLED = "CANCELLED", "CANCELLED"
        EXPIRED = "EXPIRED", "EXPIRED"

    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)

    order_status = models.CharField(max_length=100, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    order_number = models.CharField(max_length=255, blank=True, null=True)

    pick_up_at = models.CharField(max_length=255, blank=True, null=True)
    pick_up_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    deliver_to = models.CharField(max_length=255, blank=True, null=True)
    deliver_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    transit_time = models.IntegerField(blank=True, null=True)
    transit_distance = models.IntegerField(blank=True, null=True)

    line = models.CharField(max_length=255, blank=True, null=True)

    broker = models.CharField(max_length=255, blank=True, null=True)
    broker_phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
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

    match = models.IntegerField(default=0)

    coordinate_to = models.CharField(max_length=255, default="40.650002,-73.949997")
    coordinate_from = models.CharField(max_length=255, default="40.730610,-73.935242")

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.expires is None:
            raise ValidationError({"error": f"This {self.order_number} does not expire!"})

        if self.expires <= timezone.localtime(timezone.now()) and self.order_status == "PENDING":
            raise ValidationError({"error": f"This {self.order_number} order has already expired!"})

    def move_to_history(self):
        if self.user is not None:
            self.order_status = "EXPIRED"
            self.save()
            logging.info(f"------ Order {self.id} moved to history --------")
        else:
            logging.info(f"------ Order {self.id} deleted --------")
            self.delete()


class Assign(BaseModel):
    broker_company = models.CharField(max_length=255)
    rate_confirmation = models.CharField(max_length=255)
    order_id = models.OneToOneField("order.Order", on_delete=models.CASCADE, related_name="assign")

    def __str__(self):
        return f"{self.broker_company} - {self.rate_confirmation}"


class MyLoadStatus(models.Model):
    class Status(models.IntegerChoices):
        NULL = 0, "NULL"
        POINT_A = 1, "I am going to the load"
        UPLOADED = 2, "Uploaded"
        ON_THE_WAY = 3, "On the way"
        UNLOADED = 4, "Unloaded"
        DELIVERED = 5, "Delivered"
        PAID_OFF = 6, "Paid off"
        COMPLETED = 7, "Completed"

    previous_status = models.IntegerField(choices=Status.choices, default=Status.NULL)
    current_status = models.IntegerField(choices=Status.choices, default=Status.NULL)
    next_status = models.IntegerField(choices=Status.choices, default=Status.NULL)
    order = models.OneToOneField(
        "order.Order",
        on_delete=models.CASCADE,
        related_name="my_load_status",
    )

    def __str__(self):
        return f"{self.order}"


@receiver(post_save, sender=Order)
def create_status(sender, instance, created, **kwargs):
    if created:
        MyLoadStatus.objects.create(order=instance)
