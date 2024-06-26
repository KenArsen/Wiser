from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Invitation, Roles, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name", "avatar", "role")}),
        (_("Permissions"), {"fields": ("is_active", "is_superuser", "user_permissions")}),
    )
    list_filter = ["is_active", "is_superuser"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "is_active", "created_at")
    list_display_links = ("email", "first_name")
    list_editable = ("is_active",)
    search_fields = ("email",)
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ("-id",)


@admin.register(Roles)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


admin.site.register(Invitation)
