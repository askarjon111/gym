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
    def subscription(self):
        from apps.gym.models import Subscription
        subscription = Subscription.objects.filter(member=self).last()
        if subscription:
            return subscription

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def attended(self):
        from apps.gym.models import GymSession
        session = GymSession.objects.filter(member=self,
                                            start__date=datetime.now().date()).first()
        return bool(session)

    @property
    def left_sessions(self):
        from apps.gym.models import GymSession
        if self.plan:
            from apps.gym.models import Subscription
            all_sessions = self.plan.sessions
            subscription = Subscription.objects.filter(member=self).last()
            attended_sessions = GymSession.objects.filter(member=self, subscription=subscription).count()
            left = all_sessions - attended_sessions
            return left

    objects = UserManager()


class UserProfile(BaseModel):
    """Profile model for user it saves users additional information"""

    GENDER_CHOICES= (
        ('male', 'Мужской'),
        ('female', 'Женский'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    biceps = models.FloatField(blank=True, null=True)
    triceps = models.FloatField(blank=True, null=True)
    chest = models.FloatField(blank=True, null=True)
    guts = models.FloatField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=[('Trainer', 'Trainer'), ('Member', 'Member')])


    def __str__(self):
        return self.user.phone_number
