from django.urls import path

from .views import home, create_session_view

urlpatterns = [
    path('', home, name='home'),
    path('create-session/', create_session_view, name='create-session'),
]

