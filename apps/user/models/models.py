import logging
import os

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.common.enums import Role
from apps.common.image import ImageService
from apps.common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(ImageService, BaseModel, AbstractBaseUser, PermissionsMixin):
    role = models.CharField(max_length=255, choices=Role.choices)

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ("-id",)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        try:
            # if advertisement new added
            if not self.pk:
                if self.avatar:
                    # image compress
                    self.compress_image(
                        "avatar", delete_source=True, max_width=300, max_height=300
                    )
            else:
                if self.avatar:
                    # image compress
                    self.compress_image(
                        "avatar", delete_source=True, max_width=300, max_height=300
                    )

            this = User.objects.get(id=self.id)

            if not this.avatar == self.avatar:
                if os.path.isfile(this.avatar.path):
                    os.remove(this.avatar.path)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        super(User, self).save(*args, **kwargs)


@receiver(pre_delete, sender=User)
def user_avatar(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.avatar.delete(False)


class Invitation(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="invitation"
    )
    email = models.EmailField(unique=True)
    invitation_token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Приглашение"
        verbose_name_plural = "Приглашения"

    def __str__(self):
        return self.email
