from django.shortcuts import render

from apps.common.choices import STATUS_CHOICES
from apps.users.permissions import gym_manager_required


@gym_manager_required(login_url='login')
def home(request):
    gym = request.user.gym
    notifications = gym.gymnotification_set.filter(
        status=STATUS_CHOICES[0][0]).order_by('-send_at')[:5]
    return render(request, 'home.html',
                  context={"users": len(gym.members),
                           "active_members": len(gym.active_members),
                           "new_members": len(gym.new_members),
                           "notifications": notifications})
