from django.db import models
from rest_framework.exceptions import ValidationError

from apps.common.base_model import BaseModel


class Letter(BaseModel):
    order_id = models.OneToOneField("order.Order", on_delete=models.CASCADE, related_name="letter")
    driver_id = models.ForeignKey("driver.Driver", on_delete=models.CASCADE, related_name="letters")
    dispatcher_id = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="letters")
    broker_price = models.IntegerField(default=1)
    driver_price = models.IntegerField(default=1)
    comment = models.TextField(default="Empty")

    def __str__(self):
        return f"Order ID: {self.order_id.id} - Driver ID: {self.driver_id.id}"

    def clean(self):
        if not self.order_id:
            raise ValidationError({"error": "Order ID is required."})
        if not self.driver_id:
            raise ValidationError({"error": "Driver ID is required."})
        if not self.comment:
            raise ValidationError({"error": "Comment is required."})
