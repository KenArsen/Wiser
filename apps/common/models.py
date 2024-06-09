from django.db import models


class BaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class BaseManager(models.Manager.from_queryset(BaseQuerySet)):
    pass


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = BaseManager()

    class Meta:
        abstract = True

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save(update_fields=["is_active", "updated_at"])

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save(update_fields=["is_active", "updated_at"])
