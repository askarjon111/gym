from django.urls import path

from .views import home, create_session_view, PlansView, AddSubscriptionView

urlpatterns = [
    path('', home, name='home'),
    path('create-session/', create_session_view, name='create-session'),
    path('add-subscription/', AddSubscriptionView.as_view(), name='add-subscription'),
    path('plans/', PlansView.as_view(), name='plans'),
]

