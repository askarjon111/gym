from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.common.models import BaseModel
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Custom user model that supports using phone_number instead of username"""

    phone_number = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    biceps = models.FloatField(blank=True, null=True)
    triceps = models.FloatField(blank=True, null=True)
    breasts = models.FloatField(blank=True, null=True)
    guts = models.FloatField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField(blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=[('Trainer', 'Trainer'), ('Member', 'Member')])