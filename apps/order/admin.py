from django.contrib import admin

from apps.order.models.order_model import Assign, Order
from apps.order.models.template_model import Template


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "pick_up_at", "deliver_to", "user", "order_status", "my_loads_status", "order_number")
    list_display_links = ("id", "user")
    search_fields = ("email", "user__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Assign)
class AssignAdmin(admin.ModelAdmin):
    list_display = ("id", "broker_company", "order_id")
    list_display_links = ("id", "broker_company")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active")
