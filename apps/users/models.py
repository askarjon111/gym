from datetime import datetime
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser

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
    # objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number

    @property
    def plan(self) -> None:
        from apps.gym.models import Subscription
        subscription = Subscription.objects.filter(member=self).last()
        if subscription:
            return subscription.plan

    @property
    def subscription_end_date(self) -> None:
        from apps.gym.models import Subscription
        subscription = Subscription.objects.filter(member=self).last()
        if subscription:
            return subscription.end_date

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def attended(self):
        from apps.gym.models import GymSession
        session = GymSession.objects.filter(member=self,
                                            start__date__lte=datetime.now().date()).first()
        return bool(session)

    objects = UserManager()


class UserProfile(BaseModel):
    """Profile model for user it saves users additional information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    biceps = models.FloatField(blank=True, null=True)
    triceps = models.FloatField(blank=True, null=True)
    chest = models.FloatField(blank=True, null=True)
    guts = models.FloatField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField(blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=[('Trainer', 'Trainer'), ('Member', 'Member')])


    def __str__(self):
        return self.user.phone_number
