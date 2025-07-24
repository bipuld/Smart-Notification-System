from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (NotificationChannel, NotificationPreference,
                     NotificationType)

User = get_user_model()


@receiver(post_save, sender=User)
def create_default_preferences(sender, instance, created, **kwargs):
    if not created:
        return

    notification_types = NotificationType.objects.all()
    channels = NotificationChannel.values

    for notif_type in notification_types:
        for channel in channels:
            NotificationPreference.objects.get_or_create(
                user=instance,
                notification_type=notif_type,
                channel=NotificationChannel.IN_APP,
            )
