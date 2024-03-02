from django.contrib import admin
from apps.gym.models import GymProgram, GymSession, Plan, Subscription, QRCode


admin.site.register(Plan)
admin.site.register(GymProgram)


@admin.register(GymSession)
class GymSessionAdmin(admin.ModelAdmin):
    list_display = ['member', 'start', 'end']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['plan', 'member', 'start_date', 'end_date']


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'is_printed']
