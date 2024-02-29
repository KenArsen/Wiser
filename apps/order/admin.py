from django.contrib import admin

from apps.order.models.order_model import Order
from apps.order.models.template_model import Template

admin.site.register(Order)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active")
