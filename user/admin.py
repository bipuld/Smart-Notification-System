from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from user.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("-created_at",)
    list_display = (
        
        "email",
        "username",
        "full_name",
        "is_active",
        "is_verified",
        "is_staff",
    )
    list_filter = (
        "is_active",
        "is_verified",
        "is_email_verified",
    )
    search_fields = ("email", "username", "first_name", "last_name", "phone")
    readonly_fields = ("created_at", "updated_at", "password_changed_date")

    fieldsets = (
        (_("Basic Info"), {"fields": ("email", "username", "password")}),
        (
            _("Personal Details"),
            {"fields": ("first_name", "middle_name", "last_name", "phone")},
        ),
        (
            _("Verification Flags"),
            {
                "fields": (
                    "is_email_verified",
                    "is_verified",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Security and Timestamps"),
            {"fields": ("password_changed_date", "created_at", "updated_at")},
        ),
    )

    add_fieldsets = (
        (
            _("Create User"),
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "action_time",
        "user",
        "content_type",
        "colored_action",
        "object_link",
        "change_message",
    )
    list_filter = ("user", "content_type", "action_flag")
    search_fields = ("object_repr", "change_message", "user__username")
    ordering = ("-action_time",)
    readonly_fields = [f.name for f in LogEntry._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def object_link(self, obj):
        if obj.content_type and obj.object_id:
            try:
                url = f"/admin/{obj.content_type.app_label}/{obj.content_type.model}/{obj.object_id}/change/"
                return format_html('<a href="{}">{}</a>', url, obj.object_repr)
            except:
                return obj.object_repr
        return obj.object_repr

    object_link.short_description = _("Object")

    def colored_action(self, obj):
        if obj.action_flag == 1:
            color = "black"
            label = "Added"
        elif obj.action_flag == 2:
            color = "black"
            label = "Changed"
        elif obj.action_flag == 3:
            color = "black"
            label = "Deleted"
        else:
            color = "black"
            label = "Unknown"
        return format_html('<span style="color: {};">{}</span>', color, label)

    colored_action.short_description = _("Action")
