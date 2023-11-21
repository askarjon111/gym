from django.urls import path
from apps.users.views import create_user, users


urlpatterns = [
    path('', users, name="users"),
    path('add-user', create_user, name="add-user"),
]

