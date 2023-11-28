from django.contrib import admin
from apps.gym.models import GymSession, Plan, Subscription


admin.site.register(Plan)
admin.site.register(Subscription)

@admin.register(GymSession)
class GymSessionAdmin(admin.ModelAdmin):
    list_display = ['member', 'start', 'end']