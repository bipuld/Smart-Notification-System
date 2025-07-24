import logging
import re
from base64 import urlsafe_b64decode

from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from utils.email import cleanup_email

from .models import User

logger = logging.getLogger("django")
error_logger = logging.getLogger("error_logger")


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for user signup with email or phone."""

    email = serializers.EmailField(allow_blank=False, required=False)
    phone = serializers.CharField(allow_blank=False, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "middle_name",
            "last_name",
            "phone",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, password):
        pattern = r"^(?=.*?\d)(?=.*?[A-Z])(?=.*?[#?!@$%^&*\"\'()\\/{}]).{8,}$"
        if not re.match(pattern, password):
            raise ValidationError(
                "Password must be at least 8 characters long and contain:\n"
                "- at least 1 numeric character\n"
                "- at least 1 uppercase letter\n"
                "- at least 1 special character [#?!@$%^&*\"'()\\/{}]"
            )
        return password

    def validate_email(self, email):
        if not email:
            raise ValidationError("Email address is required.")
        email = cleanup_email(email)
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def validate_phone(self, phone):
        if not phone:
            raise ValidationError("Phone number is required.")

        if phone[0] != "+":
            phone = f"+{phone}"

        if User.objects.filter(phone=phone).exists():
            raise ValidationError("A user with this phone number already exists.")

        if phone.startswith("+977"):
            phone_pattern = r"^\+977(?:984|985|986|974|975|980|981|982|961|962|988|972|963|970)\d{4,12}$"
            if not re.match(phone_pattern, phone):
                raise ValidationError("Invalid Nepal phone number format.")
        return phone

    def validate(self, data):
        if not data.get("email") and not data.get("phone"):
            error_logger.error(
                "User signup failed: Neither email nor phone number provided."
            )
            raise ValidationError("Either email or phone number is required.")
        return data

    def create(self, validated_data: dict) -> User:
        """
        Create and return a new User instance with hashed password.
        Username is set to email if present, otherwise phone.
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.username = validated_data.get("email") or validated_data.get("phone")
        user.save()
        logger.info(f"User {user.username} created successfully.")

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            error_logger.error(f"Login failed: User with email {email} not found.")
            raise serializers.ValidationError("User not found.")

        if not user.check_password(password):
            error_logger.error(f"Login failed: Incorrect password for user {email}.")
            raise serializers.ValidationError("Incorrect password.")

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        refresh = RefreshToken.for_user(user)
        user.is_active = True
        user.save()
        update_last_login(None, user)
        logger.info(f"User {user.username} logged in successfully.")

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "is_staff": user.is_staff,
        }


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField(
        help_text="The refresh token to be blacklisted", required=True
    )

    def validate_refresh(self, value):
        """Validate the refresh token."""
        if not value:
            raise serializers.ValidationError("Refresh token is required.")
        return value


class CustomTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh: RefreshToken = self.token_class(attrs["refresh"])
        user: User = User.objects.get(id=refresh.payload["user_id"])
        if refresh.payload["iat"] < user.password_changed_date.timestamp():
            raise serializers.ValidationError(
                {"refresh": ["This token has already been expired."]}
            )
        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone",
            "first_name",
            "middle_name",
            "last_name",
            "is_staff",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "full_name"]
