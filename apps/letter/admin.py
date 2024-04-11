from django.contrib import admin

from .models import Letter


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'driver_id')
    list_display_links = ('id', 'order_id', 'driver_id')
    readonly_fields = ('created_at', 'updated_at')
