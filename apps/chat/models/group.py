import io

from django.core.files.storage import default_storage as storage
from django.db import models
from PIL import Image

from apps.user.models import User


def get_image_path(instance, filename):
    return f"images/{instance.name}_{filename}"


class Group(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_creator")
    description = models.TextField(max_length=300, blank=True, null=True)
    members = models.ManyToManyField(User, related_name="band_members")
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.name


def get_file_path(instance, filename):
    return f"files/{instance.group.group_name}/{filename}"


class GroupMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
