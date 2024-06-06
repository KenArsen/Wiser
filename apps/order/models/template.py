from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Template(models.Model):
    is_active = models.BooleanField(default=False)
    content = models.TextField()
    logo = models.ImageField(upload_to="orders/logos/", blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


@receiver(pre_save, sender=Template)
def set_other_templates_inactive(sender, instance, **kwargs):
    if instance.is_active:
        # Устанавливаем все остальные шаблоны в неактивное состояние
        Template.objects.exclude(id=instance.id).update(is_active=False)
