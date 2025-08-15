from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"api/(?P<version>(v1))/", include("user.urls")),
    re_path(r"api/(?P<version>(v1))/notification/", include("notification.urls")),
    path(
        "api/",
        include(
            [
                path("", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "swagger/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path(
                    "redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
            ]
        ),
    ),
    path("ckeditor5/", include("django_ckeditor_5.urls")),

]
if settings.DEBUG:
       urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
