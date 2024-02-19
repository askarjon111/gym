from django.db import models


class GymManager(models.Manager):
    def get_members(self, gym_id):
        from apps.controls.models import Gym
        gym = Gym.objects.get(id=gym_id)
        members = gym.users.filter(roles__isnull=True)
        return members

    def get_staff(self, gym_id):
        from apps.controls.models import Gym
        gym = Gym.objects.get(id=gym_id)
        staff = gym.users.filter(roles__isnull=False)
        return staff
