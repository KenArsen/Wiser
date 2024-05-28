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
    comment = models.TextField()

    def __str__(self):
        return f"{self.order}"


class Price(BaseModel):
    order = models.OneToOneField(
        "order.Order", on_delete=models.CASCADE, related_name="price"
    )
    driver = models.ForeignKey(
        "driver.Driver", on_delete=models.CASCADE, related_name="prices"
    )
    dispatcher = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="prices"
    )
    broker_price = models.PositiveIntegerField()
    driver_price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.broker_price}, {self.driver_price}"
