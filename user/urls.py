from django.urls import include, path, re_path

from .api import (CustomTokenRefreshView, LoginAPIView, LogoutAPIView,
                  SignUpView, UserListAPIView)

urlpatterns = [
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh-api"),
    path(
        "user/",
        include(
            [
                path("signup/", SignUpView.as_view(), name="user-signup"),
                path("login/", LoginAPIView.as_view(), name="user-login"),
                path("logout/", LogoutAPIView.as_view()),
                path("all/", UserListAPIView.as_view()),
            ]
        ),
    ),
]
