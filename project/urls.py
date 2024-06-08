from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions


def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('dashboard/', include('apps.gym.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('', include('apps.websites.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('sentry-debug/', trigger_error),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
