from django.contrib import admin

from .models import Vehicles


@admin.register(Vehicles)
class VehiclesAdmin(admin.ModelAdmin):
    list_display = ("id", "unit_id", "driver")
    list_display_links = ("id", "unit_id", "driver")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("driver__email", "vehicle_owner__email", "unit_id")
