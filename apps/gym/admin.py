from django.contrib import admin
from apps.gym.models import GymProgram, GymSession, Plan, Subscription


admin.site.register(Plan)
admin.site.register(GymProgram)


@admin.register(GymSession)
class GymSessionAdmin(admin.ModelAdmin):
    list_display = ['member', 'start', 'end']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['plan', 'member', 'start_date', 'end_date']
