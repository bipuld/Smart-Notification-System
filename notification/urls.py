from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (NotificationHistoryView, NotificationPreferenceViewSet,
                    NotificationReadView, NotificationTriggerView,
                    NotificationTypeList, NotificationUnReadListView)

router = DefaultRouter()
router.register(
    r"preferences", NotificationPreferenceViewSet, basename="notificationpreference"
)

urlpatterns = router.urls + [
    path(
        "notification/",
        include(
            [
                path(
                    "notifications-type/",
                    NotificationTypeList.as_view(),
                    name="notification-type-list",
                ),
                path(
                    "notification-delivery/",
                    NotificationHistoryView.as_view(),
                    name="notification-delivery",
                ),
                path(
                    "history/",
                    NotificationHistoryView.as_view(),
                    name="notification-history",
                ),
                path("read/", NotificationReadView.as_view(), name="notification-read"),
                path(
                    "unread/",
                    NotificationUnReadListView.as_view(),
                    name="notification-unread",
                ),
                path(
                    "trigger/",
                    NotificationTriggerView.as_view(),
                    name="notification-trigger",
                ),
            ]
        ),
    ),
]
