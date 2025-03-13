
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.core.exceptions import ObjectDoesNotExist
from apps.gym.forms import AddSubscriptionForm

from apps.users.models import User, UserProfile
from apps.gym.models import GymSession, Subscription
from apps.users.forms import UserProfileUpdateForm, UserUpdateForm
from apps.users.permissions import gym_manager_required
from project.settings import ERROR_PATTERN


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class UserDetail(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        try:
            user: User = get_object_or_404(User, pk=pk)
            attended_sessions = []
            list_count = 0
            gym = self.request.user.gym
            subscriptions = Subscription.objects.filter(member=user, plan__gym=gym)
            last_subscription = subscriptions.last()

            if last_subscription:
                attended_sessions = GymSession.objects.filter(
                    member=user, subscription=last_subscription)
                list_count = last_subscription.plan.sessions - attended_sessions.count()
                list_count = 0 if list_count < 0 else list_count

            add_subscription_form = AddSubscriptionForm(request=self.request)

            context = {
                'user': user,
                'attended_sessions': attended_sessions,
                'list_count': list_count,
                'add_subscription_form': add_subscription_form,
                'now': timezone.now(),
                'form': UserUpdateForm(instance=user),
                'profile_form': UserProfileUpdateForm(instance=user.profile),
                'subscriptions': subscriptions
            }

            return render(request, 'users/member.html', context)
        except ObjectDoesNotExist:
            UserProfile.objects.create(user=user)
            return redirect('user-details', user.id)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserUpdateForm(request.POST, instance=user)
        attended_sessions = GymSession.objects.filter(
            member=user, subscription=user.subscription)
        list_count = 0
        if user.plan:
            list_count = user.plan.sessions - attended_sessions.count()
        list_count = 0 if list_count < 0 else list_count
        add_subscription_form = AddSubscriptionForm(request=self.request)
        context = {
            'user': user,
            'attended_sessions': attended_sessions,
            'list_count': list_count,
            'add_subscription_form': add_subscription_form,
            'now': timezone.now(),
            'form': form
        }
        try:
            if form.is_valid():
                form.save()
                return redirect('user-details', pk=pk)
            else:
                errors = ERROR_PATTERN.search(str(form.errors)).group(1)
                messages.add_message(
                    request, messages.WARNING, f"Ошибка: {errors}")
            return render(request, 'users/member.html', context)
        except Exception as e:
            messages.add_message(self.request, messages.WARNING,
                                 f"Произошла ошибка {e}, свяжитесь с администратором.")
            return render(request, 'users/member.html', context)


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class UserDelete(View):

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if request.user != user and not request.user.is_gym_manager:
            raise PermissionDenied

        user.delete()
        messages.success(request, f"Пользователь { user.first_name } удален!")

        return redirect('users')


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class UserUpdateView(LoginRequiredMixin, FormView):
    login_url = 'login'
    template_name = 'users/member.html'
    form_class = UserUpdateForm

    def get_initial(self):
        return {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'telegram_id': self.request.user.telegram_id,
        }

    def form_valid(self, form):
        user = User.objects.get(pk=form.cleaned_data['user_id'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.phone_number = form.cleaned_data['phone_number']
        try:
            user.save()
            return redirect('dashboard')
        except Exception as e:
            print(f"{e}")
            messages.add_message(self.request, messages.WARNING,
                                 "Xatolik")
            return redirect('user-details', form.cleaned_data['user_id'])


__all__ = ['UserDetail', 'UserDelete', 'UserUpdateView']
