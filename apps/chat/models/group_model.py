import io

from django.core.files.storage import default_storage as storage
from django.db import models
from PIL import Image

from apps.user.models import User


def get_image_path(instance, filename):
    return f"images/{instance.group.group_name}_{filename}"


class Group(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator_groups")
    description = models.TextField(max_length=300, blank=True, null=True)
    members = models.ManyToManyField(User, related_name="chat_groups")
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_read = storage.open(self.image.name, "r")
        img = Image.open(img_read)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            in_mem_file = io.BytesIO()
            img.save(in_mem_file, format="JPEG")
            img_write = storage.open(self.image.name, "w+")
            img_write.write(in_mem_file.getvalue())
            img_write.close()

        img_read.close()


def get_file_path(instance, filename):
    return f"files/{instance.group.group_name}/{filename}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
