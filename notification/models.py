from django.contrib.auth import get_user_model
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from utils.base_model import TimeStampedModel

User = get_user_model()


class NotificationChannel(models.TextChoices):
    IN_APP = "in_app", "In-App"
    EMAIL = "email", "Email"
    SMS = "sms", "SMS"


class NotificationType(TimeStampedModel):
    """
    Defines the type of event that can trigger a notification, e.g., new_comment, new_login.
    """
    notification_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = CKEditor5Field(config_name="extends", blank=True)
    is_active = models.BooleanField(
        default=True, help_text="Controls if this type is currently in use."
    )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Notification Type"
        verbose_name_plural = "Notification Types"
        ordering = ["notification_code"]


class NotificationPreference(TimeStampedModel):
    """
    Tracks which user wants to receive which notification type through which channel.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(
        NotificationType, on_delete=models.CASCADE, related_name="preferences"
    )
    channel = models.CharField(max_length=20, choices=NotificationChannel.choices)

    class Meta:
        unique_together = ("user", "notification_type", "channel")
        verbose_name = "Notification Preference"
        verbose_name_plural = "Notification Preferences"
        ordering = ["user", "notification_type"]

    def __str__(self):
        return f"{self.user} - {self.notification_type.notification_code} via {self.channel}"


class Notification(TimeStampedModel):
    """
    Represents a notification event with title and message content.
    """

    notification_type = models.ForeignKey(
        NotificationType, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=255)
    content = CKEditor5Field(
        config_name="extends",
        blank=True,
        help_text="Content of the notification message.",
    )
    is_global = models.BooleanField(
        default=False,
        help_text="If True, this notification should be sent to all users.",
    )
    metadata = models.JSONField(
        blank=True,
        null=True,
        help_text="Optional structured data for dynamic notifications.",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]


class NotificationDelivery(TimeStampedModel):
    """
    Stores the delivery status of each notification for each user and channel.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name="deliveries"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=20, choices=NotificationChannel.choices)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    sent_at = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp when the notification was sent."
    )
    error_message = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(
        default=False, help_text="Marks if the user has read the in-app notification."
    )
    last_attempted_at = models.DateTimeField(
        null=True, blank=True, help_text="When the last delivery attempt occurred."
    )
    attempts = models.PositiveIntegerField(
        default=0, help_text="Number of delivery attempts made."
    )

    class Meta:
        unique_together = ("notification", "user", "channel")
        verbose_name = "Notification Delivery"
        verbose_name_plural = "Notification Deliveries"
        ordering = ["-sent_at", "user"]

    def __str__(self):
        return f"{self.user} - {self.notification.title} via {self.channel} ({self.status})"
