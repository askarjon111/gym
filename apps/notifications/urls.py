from django.urls import path

from apps.notifications.views import NotificationsListView, NotificationDetailView


urlpatterns = [
    path('', NotificationsListView.as_view(), name='notifications'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]
