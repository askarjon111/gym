from django.urls import path

from apps.notifications.views import NotificationsListView


urlpatterns = [
    path('', NotificationsListView.as_view(), name='notifications'),
]
