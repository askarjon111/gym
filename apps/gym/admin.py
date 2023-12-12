from django.contrib import admin
from apps.gym.models import GymSession, Plan, Subscription


admin.site.register(Plan)

@admin.register(GymSession)
class GymSessionAdmin(admin.ModelAdmin):
    list_display = ['member', 'start', 'end']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['plan', 'member', 'start_date', 'end_date']