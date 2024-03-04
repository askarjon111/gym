from django.utils import timezone

from django.db import models
from apps.common.choices import STATUS_CHOICES

from apps.common.models import BaseModel
from apps.users.models import User
from apps.controls.models import Gym


class Plan(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sessions = models.SmallIntegerField(default=0)
    days = models.SmallIntegerField(default=1)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Subscription(BaseModel):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['member'])
        ]

    def save(self, *args, **kwargs):
        active_subscriptions = self.member.subscription_set.filter(
            status=STATUS_CHOICES[0][0])
        if active_subscriptions.count():
            active_subscriptions.update(status=STATUS_CHOICES[1][0])

        super(Subscription, self).save(*args, **kwargs)

    def attendance_percentage(self):
        total_days = self.plan.sessions
        attended_days = self.gymsession_set.count()
        return round((attended_days / total_days) * 100 if total_days > 0 else 0)

    @property
    def used_sessions(self):
        return self.gymsession_set.count()

    @property
    def left_sessions(self):
        return self.plan.sessions - self.used_sessions if self.plan.sessions > 0 else "∞"

    def __str__(self):
        return f"{self.plan}"


class GymSession(BaseModel):
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            subscription = Subscription.objects.get(
                member=self.member,
                status=STATUS_CHOICES[0][0],
                start_date__lte=timezone.now().date(),
                end_date__gte=timezone.now().date()
            )
            self.subscription = subscription
        except Subscription.DoesNotExist:
            expired_subscriptions = Subscription.objects.filter(
                member=self.member,
                status=STATUS_CHOICES[0][0],
                end_date__lt=timezone.now().date()
            )
            if expired_subscriptions:
                expired_subscriptions.update(
                    status=STATUS_CHOICES[1][0])

            raise ValueError(
                "Member does not have a valid ongoing subscription plan.")

        if self.subscription.plan.sessions != 0 and self.subscription.plan.sessions - self.subscription.gymsession_set.all().count() <= 1:
            self.subscription.status = STATUS_CHOICES[1][0]
            self.subscription.save()

        super(GymSession, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.member}"


class QRCode(BaseModel):
    code = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to=f'qr_codes/')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    is_printed = models.BooleanField(default=False)


class GymProgram(BaseModel):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
