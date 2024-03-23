from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import User, UserProfile, GymRole, Access
from .forms import UserRegistrationForm


class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    model = User
    list_display = ['phone_number', 'first_name', 'last_name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'telegram_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'roles', 'gyms')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('phone_number',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(GymRole)
admin.site.register(Access)
