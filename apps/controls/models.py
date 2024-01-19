from datetime import timedelta
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel
from apps.gym.managers import GymManager


class GymPlan(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    members_limit = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Gym(BaseModel):
    name = models.CharField(max_length=255)
    gym_plan = models.ForeignKey(GymPlan, on_delete=models.SET_NULL,blank=True, null=True)

    objects = GymManager()

    def __str__(self):
        return self.name


    @property
    def active_subscirptions():
        """Active subsctiptions of the gym"""
        pass

    @property
    def members(self):
        """Returns all members of the gym"""
        from apps.users.models import User
        return User.objects.filter(subscription__plan__gym_id=self.id)


    @property
    def active_members(self):
        """Returns active members of the gym"""
        activity_start = timezone.now() - timedelta(days=3)
        return self.members.filter(subscription__plan__gym_id=self.id,
                                   gymsession__start__gte=activity_start).distinct()

    @property
    def new_members(self):
        """Returns new members of the gym"""
        registered = timezone.now() - timedelta(days=3)
        return self.members.filter(subscription__plan__gym_id=self.id,
                                   created_at__gte=registered)
