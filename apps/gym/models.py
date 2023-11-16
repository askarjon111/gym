from django.db import models

from apps.common.models import BaseModel
from apps.users.models import User


class Plan(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    days = models.IntegerField()


class Subscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    start_date = models.DateField()
    end_date = models.DateField()


