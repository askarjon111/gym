from django.urls import path

from .views import home, create_session_view, PlansView, AddSubscriptionView, AddNewPlanView, DeletePlanView

urlpatterns = [
    path('', home, name='home'),
    path('create-session/', create_session_view, name='create-session'),
    path('add-subscription/', AddSubscriptionView.as_view(), name='add-subscription'),
    path('add-plan/', AddNewPlanView.as_view(), name='add-plan'),
    path('plans/', PlansView.as_view(), name='plans'),
    path('plans/<int:pk>/delete/', DeletePlanView.as_view(), name='delete-plan'),
]

