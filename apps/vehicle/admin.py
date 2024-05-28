from django.contrib import admin

from .models import Location, Vehicle


class LocatoinInline(admin.StackedInline):
    model = Location
    extra = 1


@admin.register(Vehicle)
class VehiclesAdmin(admin.ModelAdmin):
    list_display = ("id", "unit_id", "driver")
    list_display_links = ("id", "unit_id", "driver")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("driver__email", "owner__email", "unit_id")
    inlines = [LocatoinInline]
