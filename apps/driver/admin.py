from django.contrib import admin

from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'email',)
    list_display_links = ('id', 'email')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('email', 'first_name', 'last_name')
