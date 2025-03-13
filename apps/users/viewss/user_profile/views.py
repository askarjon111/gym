from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from apps.users.models import UserProfile
from apps.users.forms import UserProfileUpdateForm
from apps.users.permissions import gym_manager_required


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class UserProfileUpdateView(LoginRequiredMixin, FormView):
    login_url = 'login'
    template_name = 'users/member.html'
    form_class = UserProfileUpdateForm
    success_url = 'users'

    def post(self, request, *args, **kwargs):
        profile = UserProfile.objects.filter(id=kwargs['pk']).last()
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-details', profile.user.id)
        else:
            print(form.errors)


__all__ = ['UserProfileUpdateView']
