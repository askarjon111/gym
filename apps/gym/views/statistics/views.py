from django.shortcuts import render

from apps.users.permissions import gym_manager_required


@gym_manager_required(login_url='login')
def statistics(request):
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
