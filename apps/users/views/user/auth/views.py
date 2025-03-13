
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.controls.models import Gym
from apps.users.models import User
from apps.users.forms import UserCreateForm, UserRegistrationForm
from apps.users.permissions import gym_manager_required
from apps.users.tasks import generate_and_save_access
from project.settings import ERROR_PATTERN


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class CreateUserView(View):
    model = User
    template_name = 'users/add_user.html'
    login_url = 'login'

    def post(self, request):
        form = UserCreateForm(request.POST, request=request)
        gym = self.request.user.gym
        user = User.objects.filter(
            phone_number=form.data['phone_number']).first()
        if not user:
            if form.is_valid():
                instance = form.save()
                user = User.objects.get(phone_number=instance.phone_number)
            else:
                errors = ERROR_PATTERN.search(str(form.errors)).group(1)
                messages.add_message(
                    request, messages.WARNING, f"Ошибка: {errors}")
                return redirect('add-user')
        user.gyms.add(gym)
        user.save()
        generate_and_save_access.delay(user.id)
        return redirect('add-subscription-registration', user.id)

    def get(self, request):
        return render(request, self.template_name,
                      {'form': UserCreateForm(request=request),
                       'page_title': 'Персональная информация',
                       'next_step': 'Следующий'})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class LogOutView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        logout(request)
        return redirect(self.login_url)


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class UserRegistrationView(View):
    template_name = 'users/register.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})


@api_view(['GET'])
def is_registered_view(request, tg_id):
    try:
        user = User.objects.get(telegram_id=tg_id)
        return Response({"user": user.first_name}, status=200)
    except User.DoesNotExist:
        return Response({"user": "not found"}, status=404)


@api_view(['POST'])
def register_user_view(request):
    data = request.data
    status = 400
    user, created = User.objects.get_or_create(
        phone_number=data['phone_number'],
        defaults={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'telegram_id': data['telegram_id'],
        }
    )

    if created:
        gym = Gym.objects.filter(telegram_bot_token=data['token']).first()
        print(gym)
        user.gyms.add(gym)
        user.save()
        msg, status = "Поздравляем, теперь вы один из нас!", 200
    else:
        user.telegram_id = data['telegram_id']
        user.save()
        msg, status = "Вы уже зарегистрированы!", 200
    return Response({"msg": msg}, status=status)


__all__ = ['CreateUserView', 'login_view', 'LogOutView', 'UserRegistrationView', 'is_registered_view', 'register_user_view']
