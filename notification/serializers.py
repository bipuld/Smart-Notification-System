from rest_framework import serializers

from .models import (NotificationChannel, NotificationDelivery,
                     NotificationPreference, NotificationType)


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        exclude = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return NotificationPreference.objects.create(**validated_data)


class NotificationTypeList(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]


class NotificationTriggerSerializer(serializers.Serializer):
    event = serializers.ChoiceField(
        choices=["new_comment", "new_login", "weekly_summary"],
        help_text="Type of notification event to trigger.",
    )
    data = serializers.DictField(
        child=serializers.CharField(),
        help_text="Additional data required for the event, e.g., user_id for new_login.",
    )


class NotificationDeliverySerializer(serializers.ModelSerializer):
    notification = serializers.CharField(
        source="notification.content", allow_null=True, default="No notification"
    )

    class Meta:
        model = NotificationDelivery
        fields = ["id", "notification", "is_read"]
        read_only_fields = ["id", "is_read"]


class NotificationReadSerializer(serializers.Serializer):
    notifications = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of NotificationDelivery IDs to mark as read",
    )
    
