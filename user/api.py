import logging
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (CustomTokenSerializer, LoginSerializer,
                          LogoutSerializer, SignUpSerializer, UserSerializer)

User = get_user_model()

logger = logging.getLogger("django")
error_logger = logging.getLogger("error_logger")


@extend_schema(
    summary="Signup ", description="Register new users using email or phone."
)
class SignUpView(CreateAPIView):
    """
    API  to handle user registration.
    """

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


@extend_schema(
    summary="User Login",
    description="Login with email and password to get access tokens.",
)
class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data, status=200)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view for token refresh that uses the `CustomTokenSerializer` class.

    This view extends the `TokenRefreshView` class and sets the `serializer_class` attribute to use the
    `CustomTokenSerializer` class. This allows the view to use the custom validation logic implemented in the
    `CustomTokenSerializer` class when refreshing tokens.
    """

    serializer_class = CustomTokenSerializer


@extend_schema(
    summary="User Logout",
    description="Logout by blacklisting the refresh token.",
)
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get("refresh")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )

        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(ListAPIView):
    """API to list all users."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
