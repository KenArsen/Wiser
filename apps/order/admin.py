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
    list_display = ("id", "user", "status", "order_number")
    list_display_links = ("id", "user")
    search_fields = ("email", "user__email")
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
