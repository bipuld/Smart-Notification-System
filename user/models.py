import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError as RestValidationError

from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    username = models.CharField(_("username"), max_length=255, unique=True)
    phone = models.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex=r"^\+?[1-9][0-9]{7,14}$",
                message="The contact number can have + sign in the beginning and max 15 digits without delimiters",
            )
        ],
        null=True,
        blank=True,
    )
    first_name = models.CharField(_("first name"), max_length=64, null=True, blank=True)
    middle_name = models.CharField(
        _("middle name"), max_length=64, null=True, blank=True
    )
    last_name = models.CharField(_("last name"), max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name="Active Status")
    location= models.CharField(
        _("location"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("The location of the user, e.g., city or country."),
    )
    is_email_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False, verbose_name="Verified Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    password_changed_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-created_at", "first_name")
        permissions = (("view_user_analytics", "Can view user analytics"),)

    def __str__(self):
        return f"{self.username} ({self.email})" if self.email else self.username

    def get_full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(filter(None, parts)).strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def clean(self):
        super().clean()
        self.username = self.username.lower()
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)

    def get_saved_by_users(self):
        return User.objects.filter(bookmark__in=self.bookmarks.all())

    @property
    def full_name(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except (ValidationError, IntegrityError) as e:
            raise RestValidationError(e) from e
