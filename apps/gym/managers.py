from django.db import models


class GymManager(models.Manager):
    def get_members(self, gym_id):
        from apps.users.models import User
        return User.objects.filter(subscription__plan__gym_id=gym_id).distinct()

    def get_staff(self, gym_id):
        from apps.users.models import User
        return User.objects.filter(gym__id=gym_id)
