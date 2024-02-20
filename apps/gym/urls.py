from django.urls import path

from .views.main import home, PlansView, AddSubscriptionView, AddNewPlanView, ArchivePlanView
from .views.statistics import statistics

urlpatterns = [
    path('', home, name='home'),
    path('add-subscription/', AddSubscriptionView.as_view(), name='add-subscription'),
    path('add-plan/', AddNewPlanView.as_view(), name='add-plan'),
    path('plans/', PlansView.as_view(), name='plans'),
    path('plans/<int:pk>/archive/', ArchivePlanView.as_view(), name='archive-plan'),
    path('statistics/', statistics, name="statistics")
]

