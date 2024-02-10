from datetime import timedelta
from django.db import models
from django.utils import timezone
from apps.common.choices import NOTIFICATION_TYPE_CHOICES, STATUS_CHOICES

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
    gym_plan = models.ForeignKey(
        GymPlan, on_delete=models.SET_NULL, blank=True, null=True)

    objects = GymManager()

    def __str__(self):
        return self.name

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

    @property
    def plans(self):
        """Returns all plans of the gym"""
        from apps.gym.models import Plan
        return Plan.objects.filter(gym__id=self.id)


# class GymInvoice(BaseModel):
#     STATUS_CHOICES = (
#         ('paid', 'Оплаченный'),
#         ('peding', 'Ожидание'),
#         ('canceled', 'Отменено'),
#     )
#     status = models.CharField(
#         max_length=15, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
#     gym = models.ForeignKey(Gym, on_delete=models.CASCADE)


class GymSubscription(BaseModel):
    plan = models.ForeignKey(GymPlan, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    start_date = models.DateField()
    end_date = models.DateField()


class GymNotification(BaseModel):
    title = models.CharField(max_length=250)
    body = models.TextField(blank=True, null=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    send_at = models.DateTimeField(null=True)
    type = models.CharField(max_length=7,
                            choices=NOTIFICATION_TYPE_CHOICES,
                            default=NOTIFICATION_TYPE_CHOICES[0][0])
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return self.title
    
