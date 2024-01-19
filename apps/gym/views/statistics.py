from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.controls.models import Gym
from apps.gym.forms import AddNewPlanForm, AddSubscriptionForm


from apps.gym.models import GymSession, Plan, Subscription
from apps.users.models import User
from apps.users.permissions import gym_manager_required


@gym_manager_required(login_url='login')
def satistics(request):
    gym = request.user.gym

    if gym:
        context = {
            'all_members': len(gym.members),
            'active_members': len(gym.active_members),
            'new_members': len(gym.new_members)
        }

        return render(request, 'gym/statistics.html', context)
    else:
        return render(request, 'gym/no_gym_association.html')
