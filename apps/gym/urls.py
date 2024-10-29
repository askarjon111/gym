from django.urls import path

from .views.statistics import statistics
from .views.plan import UpdatePlanView, PlansView, AddNewPlanView, ArchivePlanView, get_plan_days
from .views.subscription import AddSubscriptionView,  cancel_subscription
from .views.equipment import AddNewGymEquipmentView, EquipmentView, remove_equipment


urlpatterns = [
    path('subscription/add/', AddSubscriptionView.as_view(),
         name='add-subscription'),
    path('subscription/add/<int:pk>/', AddSubscriptionView.as_view(),
         name='add-subscription-registration'),
    path('subscriptions/<int:sub_id>/cancel/',
         cancel_subscription, name='cancel-subscription'),

    path('equipment/', EquipmentView.as_view(), name='equipment'),
    path('equipment/add', AddNewGymEquipmentView.as_view(), name='add-equipment'),
    path('equipment/<int:pk>/delete', remove_equipment, name='delete-equipment'),

    path('plans/', PlansView.as_view(), name='plans'),
    path('plan/add/', AddNewPlanView.as_view(), name='add-plan'),
    path('plans/<int:plan_id>/days/', get_plan_days, name='get-plan-days'),
    path('plans/<int:pk>/archive/', ArchivePlanView.as_view(), name='archive-plan'),
    path('plans/<int:pk>/update/', UpdatePlanView.as_view(), name='update-plan'),

    path('statistics/', statistics, name="statistics"),
]
