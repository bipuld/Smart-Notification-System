from django.contrib import admin

from .models import (Notification, NotificationDelivery,
                     NotificationPreference, NotificationType)


@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "notification_code", "name", "is_active")
    search_fields = ("notification_code", "name")
    list_filter = ("is_active",)

    fieldsets = (
        (None, {"fields": ("notification_code", "name", "description")}),
        ("Settings", {"fields": ("is_active",)}),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "notification_type", "channel")
    list_filter = ("channel",)
    search_fields = ("user__email", "notification_type__notification_code")

    fieldsets = ((None, {"fields": ("user", "notification_type", "channel")}),)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "notification_type", "is_global", "created_at")
    search_fields = ("title", "content")
    list_filter = ("is_global",)

    fieldsets = (
        (None, {"fields": ("title", "notification_type", "content")}),
        ("Advanced Options", {"fields": ("is_global", "metadata")}),
    )


@admin.register(NotificationDelivery)
class NotificationDeliveryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "notification",
        "user",
        "channel",
        "status",
        "sent_at",
        "is_read",
    )
    list_filter = ("status", "channel", "is_read")
    search_fields = ("user__email", "notification__title")

    fieldsets = (
        (None, {"fields": ("notification", "user", "channel")}),
        (
            "Delivery Status",
            {
                "fields": (
                    "status",
                    "is_read",
                    "sent_at",
                    "last_attempted_at",
                    "attempts",
                    "error_message",
                )
            },
        ),
    )
    readonly_fields = ("sent_at", "last_attempted_at", "attempts", "error_message")
