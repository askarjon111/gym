from django.urls import path

from .views.main import home, PlansView, AddSubscriptionView, \
    AddNewPlanView, ArchivePlanView, get_plan_days, cancel_subscription
from .views.statistics import statistics

urlpatterns = [
    path('', home, name='dashboard'),
    path('add-subscription/', AddSubscriptionView.as_view(),
         name='add-subscription'),
    path('subscriptions/<int:sub_id>/cancel/',
         cancel_subscription, name='cancel-subscription'),
    path('add-plan/', AddNewPlanView.as_view(), name='add-plan'),
    path('plans/', PlansView.as_view(), name='plans'),
    path('plans/<int:plan_id>/days/', get_plan_days, name='get-plan-days'),
    path('plans/<int:pk>/archive/', ArchivePlanView.as_view(), name='archive-plan'),
    path('statistics/', statistics, name="statistics"),
]
