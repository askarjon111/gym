from django.urls import path

from .views.main import home, PlansView, AddSubscriptionView, AddNewPlanView, DeletePlanView
from .views.statistics import satistics

urlpatterns = [
    path('', home, name='home'),
    path('add-subscription/', AddSubscriptionView.as_view(), name='add-subscription'),
    path('add-plan/', AddNewPlanView.as_view(), name='add-plan'),
    path('plans/', PlansView.as_view(), name='plans'),
    path('plans/<int:pk>/delete/', DeletePlanView.as_view(), name='delete-plan'),
    path('statistics/', satistics, name="statistics")
]

