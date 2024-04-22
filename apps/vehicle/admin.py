from django.contrib import admin

from apps.user.models import User

from .models import Vehicles


class DispatcherVehiclesFilter(admin.SimpleListFilter):
    title = "Диспетчерские транспортные средства"
    parameter_name = "dispatcher_vehicles"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Да"),
            ("no", "Нет"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            dispatchers = User.objects.filter(role="DISPATCHER")
            return queryset.filter(driver__user__in=dispatchers)
        elif self.value() == "no":
            return queryset.exclude(driver__user__role="DISPATCHER")
        else:
            return queryset


@admin.register(Vehicles)
class VehiclesAdmin(admin.ModelAdmin):
    list_display = ("id", "unit_id", "driver")
    list_display_links = ("id", "unit_id", "driver")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("driver__email", "vehicle_owner__email", "unit_id")
    list_filter = [DispatcherVehiclesFilter]
