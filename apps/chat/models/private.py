from django.db import models


class Private(models.Model):
    sender = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="private_sender")
    receiver = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="private_receiver")

    def __str__(self):
        return f"{self.id}"


def get_file_path(instance, filename):
    return f"files/{filename}"


class PrivateMessage(models.Model):
    private = models.ForeignKey(Private, on_delete=models.CASCADE, related_name="chat_messages")
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
