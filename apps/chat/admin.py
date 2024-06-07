from django.contrib import admin

from .models import Group, GroupMessage, Private, PrivateMessage


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(GroupMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender")
    list_display_links = ("id", "sender")


@admin.register(Private)
class PrivateAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver")
    list_display_links = ("id", "sender", "receiver")


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "private", "content", "file")
    list_display_links = ("id", "private", "content", "file")
