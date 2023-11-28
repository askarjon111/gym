from datetime import datetime
from django.db import models

from apps.common.models import BaseModel
from apps.users.models import User


class Plan(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    days = models.IntegerField()

    def __str__(self):
        return self.name


class Subscription(BaseModel):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.plan}"
    


class GymSession(BaseModel):
    start = models.DateTimeField(default=datetime.now())
    end = models.DateTimeField(default=datetime.now())
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        try:
            Subscription.objects.get(
                member=self.member,
                status='Active',
                start_date__lte=datetime.now().date(),
                end_date__gte=datetime.now().date()
            )
        except Subscription.DoesNotExist:
            raise ValueError("Member does not have a valid ongoing subscription plan.")

        super(GymSession, self).save(*args, **kwargs)

    def __str__(self):
        return self.member
    
