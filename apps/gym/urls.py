from django.urls import path

from .views import home, create_session_view, PlansView

urlpatterns = [
    path('', home, name='home'),
    path('create-session/', create_session_view, name='create-session'),
    path('plans/', PlansView.as_view(), name='plans'),
]

