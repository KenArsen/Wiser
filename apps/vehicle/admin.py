from django.contrib import admin

from .models import Vehicle


@admin.register(Vehicle)
class VehiclesAdmin(admin.ModelAdmin):
    list_display = ("id", "unit_id", "transport_type", "vehicle_model", "vin", "driver", "owner", "dispatcher")
    list_display_links = ("id", "unit_id", "transport_type", "vehicle_model", "vin", "driver", "owner", "dispatcher")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("unit_id", "vehicle_model", "transport_type", "vehicle_year", "vin")
    list_filter = ("transport_type", "vehicle_year", "vehicle_model", "dispatcher", "owner")
