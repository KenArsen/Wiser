from django.db import models

from apps.common.models import BaseModel


class Letter(BaseModel):
    order = models.OneToOneField(
        "order.Order", on_delete=models.CASCADE, related_name="letter"
    )
    driver = models.ForeignKey(
        "driver.Driver", on_delete=models.CASCADE, related_name="letters"
    )
    dispatcher = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="letters"
    )
    broker_price = models.PositiveIntegerField()
    driver_price = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.order}"
