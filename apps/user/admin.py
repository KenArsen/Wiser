from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User, Invitation, Roles


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'avatar', 'roles')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'user_permissions')}),
    )
    list_filter = ['is_active', 'is_superuser']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'is_active', 'created_at')
    list_display_links = ('email', 'first_name')
    list_editable = ('is_active',)
    search_fields = ('email',)
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ('-id',)


admin.site.register(User, UserAdmin)
admin.site.register(Invitation)
admin.site.register(Roles)
