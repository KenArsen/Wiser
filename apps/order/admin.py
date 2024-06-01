from django.contrib import admin

from apps.order.models import Assign, File, Letter, Order, Template


class LetterInline(admin.StackedInline):
    model = Letter
    extra = 1


class FileInline(admin.StackedInline):
    model = File
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order_number", "broker", "broker_email", "status")
    list_display_links = ("id", "order_number", "broker", "broker_email", "status")
    search_fields = ("order_number", "broker", "broker_email")
    list_filter = ("status", "user")
    readonly_fields = ("created_at", "updated_at")
    inlines = [LetterInline, FileInline]


@admin.register(Assign)
class AssignAdmin(admin.ModelAdmin):
    list_display = ("id", "broker_company", "order")
    list_display_links = ("id", "broker_company")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active")
