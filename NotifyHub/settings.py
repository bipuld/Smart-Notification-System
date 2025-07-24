import os
from datetime import timedelta
from pathlib import Path

from decouple import config
import dj_database_url




BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-79atm*%u3fsbymr#gn^dq5(+awya7ti&2a4%x=+@3fayefvl8#"

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,*", cast=lambda v: [s.strip() for s in v.split(",")])
os.environ["DJANGO_RUNSERVER_HIDE_WARNING"] = "true"  # Disable runserver warning

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "user",
    "notification",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework_simplejwt.token_blacklist",
]
EXTERNAL_APPS = [
    "jazzmin",
    "django_ckeditor_5",
]

INSTALLED_APPS = EXTERNAL_APPS + INSTALLED_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "NotifyHub.urls"
AUTH_USER_MODEL = "user.User"  # Custom user model

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "NotifyHub.wsgi.application"
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}
# JWT Authentication settings

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("ACCESS_TOKEN_LIFETIME_MINUTES", default=5, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        minutes=config("REFRESH_TOKEN_LIFETIME_MINUTES", default=15, cast=int)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    # Requires 'rest_framework_simplejwt.token_blacklist' to be added in installed apps
    # 'BLACKLIST_AFTER_ROTATION': True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="notify"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="root"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' 
STATICFILES_DIRS = [
    BASE_DIR / 'static',  
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# media file settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Swagger configuration

SPECTACULAR_SETTINGS = {
    "TITLE": "Smart Notification System API",
    "DESCRIPTION": "Smart Notification System API Documentation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "CAMELIZE_NAMES": True,
    "SCHEMA_PATH_PREFIX": r"/api/{version}/",
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        "displayRequestDuration": True,
        "filter": True,
        "tryItOutEnabled": True,
        "defaultModelsExpandDepth": -1,
    },
}

# Logger configuration

LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, ".", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "timestamp": {
            "format": "{asctime} {levelname} {message} {lineno}",
            "style": "{",
        },
    },
    "handlers": {
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "debug.log"),
            "formatter": "timestamp",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "error.log"),
            "formatter": "timestamp",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["debug_file"],
            "level": "INFO",
            "propagate": True,
        },
        "error_logger": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
# Jazzmin configuration for NotifyHub Admin
JAZZMIN_SETTINGS = {
    # Title of the site in browser tab
    "site_title": "NotifyHub Admin",
    # Title shown on the login screen and header
    "site_header": "NotifyHub Administration",
    # Branding for the top left corner
    "site_brand": "NotifyHub",
    # Path to custom favicon (uncomment and add your favicon if needed)
    # "site_icon": "images/favicon.ico",
    # Welcome text shown to users on the login screen
    "welcome_sign": "Welcome to NotifyHub Admin",
    # Whether to show the sidebar on the left
    "show_sidebar": True,
    # Whether navigation should be expanded by default
    "navigation_expanded": True,
    # Custom icons for your apps/models
    "icons": {
        "core.User": "fas fa-user",
        "core.Notification": "fas fa-bell",
        "core.Message": "fas fa-envelope",
        "core.Subscriber": "fas fa-user-friends",
        "auth": "fas fa-users-cog",  # default Django auth app
    },
    # Default icon for parent modules (like groups of models)
    "default_icon_parents": "fas fa-folder-open",
    # Default icon for child links in the menu
    "default_icon_children": "fas fa-angle-right",
    # Use custom CSS for admin panel styling (optional)
    # "custom_css": "css/admin_custom.css",
    # Form layout style on model change forms
    "changeform_format": "horizontal_tabs",  # Can be 'collapsible', 'horizontal_tabs', 'vertical_tabs', or 'carousel'
    # Override layout per specific model
    "changeform_format_overrides": {
        "core.User": "collapsible",
        "core.Notification": "vertical_tabs",
    },
}
