import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Notification, NotificationChannel, NotificationDelivery,
                     NotificationPreference, NotificationType)
from .serializers import (NotificationDeliverySerializer,
                          NotificationPreferenceSerializer,
                          NotificationReadSerializer,
                          NotificationTriggerSerializer, NotificationTypeList)

User = get_user_model()
logger = logging.getLogger("django")
error_log = logging.getLogger("error_logger")

@extend_schema(tags=["Notification Preferences"])
class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


@extend_schema(tags=["Notifications Trigger"])
class NotificationTriggerView(APIView):
    """
    API endpoint to simulate or trigger notification events manually
    For now this event can be only trigrred by the admin user only.
    """

    permission_classes = [IsAdminUser]
    serializer_class = NotificationTriggerSerializer

    SUPPORTED_EVENTS = ["new_comment", "new_login", "weekly_summary"]

    def post(self, request, *args, **kwargs):
        serializer = NotificationTriggerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event_code = serializer.validated_data["event"]
        data = serializer.validated_data["data"]

        logger.info(f"Notification trigger requested: event={event_code}, data={data}")

        if event_code not in self.SUPPORTED_EVENTS:
            logger.warning(f"Unsupported event type: {event_code}")
            return Response(
                {"error": "Invalid or unsupported event name."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            notify_type = NotificationType.objects.get(notification_code=event_code)
        except NotificationType.DoesNotExist:
            logger.error(f"Notification type not found: {event_code}")
            return Response(
                {"error": "Notification type not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        message = self._generate_message(event_code, data)
        logger.info(f"Generated message for event {event_code}: {message}")

        with transaction.atomic():
            notification = Notification.objects.create(
                notification_type=notify_type,
                title=notify_type.name,
                content=message,
                is_global=True if event_code != "new_login" else False,
                created_at=timezone.now(),
            )

            logger.info(f"Notification created: id={notification.id}")
            # Determine recipients based on event type for specific notifications event new_login for provided user_id
            # For other events, we assume all users should receive the notification.
            users = self._get_target_users(event_code, data)
            logger.info(f"Target users: {[user.id for user in users]}")

            # Deliver the notification to users based on their preferences provided
            delivery_count = self._create_deliveries(notification, notify_type, users)

        return Response(
            {
                "detail": f"Notification triggered: {delivery_count} deliveries created.",
                "notification_id": notification.id,
            },
            status=status.HTTP_200_OK,
        )

    def _generate_message(self, event_code: str, data: dict) -> str:
        """
        Dynamically generates message content based on event type.
        """
        if event_code == "new_comment":
            return f"New comment posted: {data.get('comment', '(no content)')}"
        elif event_code == "new_login":
            return "New login from an unrecognized device."
        elif event_code == "weekly_summary":
            return "Here is your weekly summary."
        return "Notification."

    def _get_target_users(self, event_code: str, data: dict):
        """
        Resolves which users should receive the notification.
        """
        if event_code == "new_login":
            user_id = data.get("user_id")
            if user_id:
                return User.objects.filter(id=user_id)
            return User.objects.none()
        else:
            return User.objects.all()

    def _create_deliveries(self, notification, notif_type, users) -> int:
        """
        For each user, checks preferences and creates a delivery per channel.
        """
        count = 0
        for user in users:
            #As the NotificationPreference model is already created with all provided channels if not 
            # provided, we can directly Create Notification Preference accordg to the user and notification type and channels.
            #TODO: This should be handled in a separate management command or signal to avoid duplication.
            # This is a mockup, in real case you would check existing preferences.
            # For simplicity, we assume all users have preferences set for in_app channels.
            preferences = NotificationPreference.objects.filter( 
                user=user,
                notification_type=notif_type,
            )

            for pref in preferences:
                # Create a delivery record for each channel preference and make it ready to send for now simulating the send.
                # TODO:In Future Notifiation is Send accordingly choosen channel and using scheduler to send faile status messages and track attempts and throttle them.
                delivery = NotificationDelivery.objects.create(
                    notification=notification,
                    user=user,
                    channel=pref.channel,
                )
                self._mock_send(delivery)
                count += 1

        logger.info(f"Total deliveries created: {count}")
        return count

    def _mock_send(self, delivery: NotificationDelivery):
        """
        Simulates sending a notification based on channel.
        This is where real integration (email, SMS) would go.
        """
        try:
            if delivery.channel == NotificationChannel.IN_APP:
                logger.debug(f"In-app notification queued for user={delivery.user.id}")
            elif delivery.channel == NotificationChannel.EMAIL:
                logger.debug(
                    f"[MOCK EMAIL] To: {delivery.user.email} - {delivery.notification.content}"
                )
            elif delivery.channel == NotificationChannel.SMS:
                recipient = getattr(
                    delivery.user, "phone_number", delivery.user.username
                )
                logger.debug(
                    f"[MOCK SMS] To: {recipient} - {delivery.notification.content}"
                )
            # simulation the sending message as sent 
            # TODO:Wherever,Later we will use actual sending logic for failure.

            delivery.status = "sent" 

            delivery.sent_at = timezone.now()
            logger.info(
                f"Delivery marked as sent: user={delivery.user.id}, channel={delivery.channel}"
            )

        except Exception as e:
            delivery.status = "failed"
            delivery.error_message = str(e)
            logger.error(
                f"Failed to send notification: user={delivery.user.id}, "
                f"channel={delivery.channel}, error={e}"
            )

        delivery.save()
#For Now NotificationTypeList is used to list all the notification types available in the system.
#TODO:In Future, we can create a NotificationType API to create new notification types.
@extend_schema(tags=["Notifications View"])
class NotificationTypeList(ListAPIView):
    """This view lists all notification types"""

    serializer_class = NotificationTypeList
    queryset = NotificationType.objects.all()
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Notifications View"])
class NotificationHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationDeliverySerializer
    queryset = NotificationDelivery.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)



@extend_schema(tags=["Notifications View"])
class NotificationUnReadListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationDeliverySerializer
    queryset = NotificationDelivery.objects.all()

    def get_queryset(self):
        print(self.request.user)
        return self.queryset.filter(
            user=self.request.user, is_read=False, channel="in_app"
        )
@extend_schema(tags=["Notifications View"])
class NotificationReadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationReadSerializer
    queryset = NotificationDelivery.objects.all()

    def post(self, request, *args, **kwargs):
        """Mark specified notifications as read."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notifications = serializer.validated_data["notifications"]

        #The notifications is made to is_read  as defualt as channel in_app logically but if require email or sms we can add that logic here.
        # For now, we are only marking in-app notifications as read.
        try:
            updated_count = NotificationDelivery.objects.filter(
                user=self.request.user, id__in=notifications, channel="in_app"
            ).update(is_read=True)
            return Response(
                {"detail": f"Marked {updated_count} notifications as read."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"messages": {"error": f"Failed to update notifications: {str(e)}"}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )