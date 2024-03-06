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
        POINT_A = "A", "Выехал на точку А"
        LOADED = "B", "Загрузил"
        ON_THE_WAY = "C", "В дороге"
        UNLOADED = "D", "Выгрузил"

    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)
    from_whom = models.EmailField(null=True, blank=True)

    is_active = models.BooleanField(default=True, null=True, blank=True)
    order_status = models.CharField(max_length=100, choices=OrderStatus.choices, default=OrderStatus.DEFAULT)

    pick_up_at = models.CharField(max_length=255, blank=True, null=True)
    pick_up_date_CEN = models.DateTimeField(blank=True, null=True, default=timezone.now)
    pick_up_date_EST = models.DateTimeField(blank=True, null=True, default=timezone.now)

    deliver_to = models.CharField(max_length=255, blank=True, null=True)
    deliver_date_CEN = models.DateTimeField(blank=True, null=True, default=timezone.now)
    deliver_date_EST = models.DateTimeField(blank=True, null=True, default=timezone.now)

    notes = models.CharField(max_length=400, blank=True, null=True)
    miles = models.FloatField(blank=True, null=True)
    pieces = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    dims = models.CharField(max_length=255, blank=True, null=True)

    stackable = models.CharField(max_length=255, blank=True, null=True)
    hazardous = models.CharField(max_length=255, blank=True, null=True)
    fast_load = models.CharField(max_length=255, blank=True, null=True)
    dock_level = models.CharField(max_length=255, blank=True, null=True)

    suggested_truck_size = models.CharField(max_length=255, blank=True, null=True)

    this_posting_expires_cen = models.DateTimeField(
        blank=True, null=True, default=timezone.now
    )
    this_posting_expires_est = models.DateTimeField(
        blank=True, null=True, default=timezone.now
    )

    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    company_location = models.CharField(max_length=255, blank=True, null=True)
    company_phone = models.CharField(max_length=40, blank=True, null=True)

    load_posted_by = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    order_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.from_whom

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if not self.order_number:
            raise exceptions.ValidationError({"error": "This order number cannot be empty"})

        if Order.objects.filter(order_number=self.order_number).exists():
            raise exceptions.ValidationError({"error": "This order number is already in use"})

        if self.this_posting_expires_est is None:
            raise exceptions.ValidationError({"error": f"Срок действия этого {self.id} нет!"})

        if self.this_posting_expires_est <= timezone.localtime(timezone.now()):
            raise exceptions.ValidationError({"error": f"Срок действия этого {self.id} заказа уже истек!"})

    def move_to_history(self):
        if self.user is not None:
            self.is_active = False
            self.save()
            logging.info(f"------ Заказ {self.id} перемещен в историю --------")
        else:
            logging.info(f"------ Заказ {self.id} удален --------")
            self.delete()
