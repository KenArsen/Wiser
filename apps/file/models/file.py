from django.db import models
from django.utils.timezone import now

from apps.common.models import BaseModel


def get_file_path(instance, filename):
    date = now()
    return f"files/{date.year}/{date.month}/{date.day}/order_id_{instance.order.id}/{filename}"


class File(BaseModel):
    order = models.ForeignKey("order.Order", on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=get_file_path)

    def __str__(self):
        return f"{self.file.name}"
