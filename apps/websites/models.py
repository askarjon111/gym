from django.db import models
from apps.common.models import BaseModel
from apps.controls.models import Gym


class GymWebsite(BaseModel):
    gym = models.OneToOneField(Gym, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    subdomain = models.CharField(max_length=20, unique=True)
