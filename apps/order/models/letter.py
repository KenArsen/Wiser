from django.db import models

from apps.common.models import BaseModel
from apps.driver.models import Driver

from .order import Order


class Letter(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="letter")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="letters")
    broker_price = models.PositiveIntegerField(blank=True, null=True)
    driver_price = models.PositiveIntegerField(blank=True, null=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.order}"
