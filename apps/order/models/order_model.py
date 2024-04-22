import logging

from django.db import models
from django.utils import timezone
from rest_framework import exceptions

from apps.common.base_model import BaseModel


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        DEFAULT = "DEFAULT", "----"
        PENDING = "PENDING", "Pending"
        MY_LOADS = "MY_LOADS", "My Loads"

    class MyLoadsStatus(models.IntegerChoices):
        DEFAULT = 0, "Active"
        POINT_A = 1, "I am going to the load"
        UPLOADED = 2, "Uploaded"
        ON_THE_WAY = 3, "On the way"
        UNLOADED = 4, "Unloaded"
        DELIVERED = 5, "Delivered"
        CHECKOUT = 6, "Checkout"
        COMPLETED = 7, "Completed"

    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True, null=True, blank=True)

    order_status = models.CharField(max_length=100, choices=OrderStatus.choices, default=OrderStatus.DEFAULT)
    my_loads_status = models.IntegerField(choices=MyLoadsStatus.choices, default=MyLoadsStatus.DEFAULT)

    order_number = models.CharField(max_length=255, blank=True, null=True)

    pick_up_at = models.CharField(max_length=255, blank=True, null=True)
    pick_up_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    deliver_to = models.CharField(max_length=255, blank=True, null=True)
    deliver_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

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

    coordinate_to = models.CharField(max_length=255, default="40.650002, -73.949997")
    coordinate_from = models.CharField(max_length=255, default="40.730610, -73.935242")

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.expires is None:
            raise exceptions.ValidationError({"error": f"Срок действия этого {self.order_number} нет!"})

        if self.expires <= timezone.localtime(timezone.now()):
            raise exceptions.ValidationError({"error": f"Срок действия этого {self.order_number} заказа уже истек!"})

    def move_to_history(self):
        if self.user is not None:
            self.is_active = False
            self.save()
            logging.info(f"------ Заказ {self.id} перемещен в историю --------")
        else:
            logging.info(f"------ Заказ {self.id} удален --------")
            self.delete()


class Assign(BaseModel):
    broker_company = models.CharField(max_length=255)
    rate_confirmation = models.CharField(max_length=255)
    order_id = models.OneToOneField("order.Order", on_delete=models.CASCADE, related_name="assign")

    def __str__(self):
        return f"{self.broker_company} - {self.rate_confirmation}"
