from django.db import models
from apps.common.models import BaseModel


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

    def __str__(self):
        return self.name
