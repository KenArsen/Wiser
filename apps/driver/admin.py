from django.contrib import admin

from apps.vehicle.models import Vehicle

from .models import Driver


class VehicleInline(admin.StackedInline):
    model = Vehicle
    extra = 1


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "ssn")
    list_display_links = ("id", "email", "first_name", "last_name", "ssn")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("email", "first_name", "last_name", "ssn", "city")
    list_filter = ("type", "is_available")
    inlines = [VehicleInline]
