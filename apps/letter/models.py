from django.db import models
from apps.common.base_model import BaseModel
from rest_framework.exceptions import ValidationError


class Letter(BaseModel):
    order_id = models.ForeignKey('order.Order', on_delete=models.CASCADE, default=1, related_name='letters')
    driver_id = models.ForeignKey('driver.Driver', on_delete=models.CASCADE, default=1, related_name='letters')
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.comment[:30]}... '

    def clean(self):
        if not self.order_id:
            raise ValidationError({'error': 'Order ID is required.'})
        if not self.driver_id:
            raise ValidationError({'error': 'Driver ID is required.'})