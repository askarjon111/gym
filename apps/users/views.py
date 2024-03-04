from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.common.choices import STATUS_CHOICES
from apps.controls.models import Gym
from apps.gym.forms import AddSubscriptionForm

from apps.users.models import User
from apps.gym.models import GymSession, Plan, Subscription
from apps.users.forms import AttendanceForm, UserCreateForm, UserRegistrationForm, UserUpdateForm
from apps.users.permissions import gym_manager_required


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class CreateUser(View):
    model = User
    template_name = 'users/add_user.html'
    login_url = 'login'

    def post(self, request):
        form = UserCreateForm(request.POST, request=request)
        if form.is_valid():
            gym = self.request.user.gym
            instance = form.save()
            user = User.objects.get(phone_number=instance.phone_number)
            user.gyms.add(gym)
            user.save()

        else:
            print(form.errors)
            return redirect('add-user')
        return redirect('add-subscription-registration', user.id)

    def get(self, request):
        return render(request, self.template_name,
                      {'form': UserCreateForm(request=request),
                       'page_title': 'Персональная информация',
                       'next_step': 'Следующий'})


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class MembersListView(LoginRequiredMixin, View):
    template_name = 'users/members.html'
    context_object_name = 'objects'
    paginate_by = 20
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        gym = self.request.user.gym
        if gym:
            users = Gym.objects.get_members(gym.id).order_by('-id')
        now = timezone.now()

        if query:
            users = users.filter(
                Q(phone_number__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        paginator = Paginator(users, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        form = AttendanceForm()
        return render(request, self.template_name, {'objects': users,
                                                    'form': form,
                                                    'now': now,
                                                    'add_subscription_form':
                                                    AddSubscriptionForm(request=self.request)})

    def post(self, request, *args, **kwargs):
        form = AttendanceForm(request.POST, request=request)
        if form.is_valid():
            form.save(start=timezone.now())
            referer = request.META.get('HTTP_REFERER')
            if referer and reverse('user-details', args=[str(request.POST['member'])]) in referer:
                return redirect(referer)
            else:
                return redirect('users')

        return render(request, self.template_name, {'members': User.objects.all().order_by('-id'), 'form': form})


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class StaffListView(LoginRequiredMixin, View):
    template_name = 'users/staff.html'
    context_object_name = 'objects'
    paginate_by = 20
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        gym = self.request.user.gym
        if gym:
            members = Gym.objects.get_staff(gym.id).order_by('-id')
        now = timezone.now()

        if query:
            members = members.filter(
                Q(phone_number__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        paginator = Paginator(members, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            members = paginator.page(page)
        except PageNotAnInteger:
            members = paginator.page(1)
        except EmptyPage:
            members = paginator.page(paginator.num_pages)

        form = AttendanceForm()
        return render(request, self.template_name, {'members': members,
                                                    'form': form,
                                                    'now': now,
                                                    'add_subscription_form': AddSubscriptionForm(request=self.request)})

    def post(self, request, *args, **kwargs):
        form = AttendanceForm(request.POST, request=request)
        if form.is_valid():
            form.save(start=timezone.now())
            referer = request.META.get('HTTP_REFERER')
            if referer and reverse('user-details', args=[str(request.POST['member'])]) in referer:
                return redirect(referer)
            else:
                return redirect('users')

        return render(request, self.template_name, {'members': User.objects.all().order_by('-id'), 'form': form})


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class UserDetail(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        attended_sessions = []
        list_count = 0

        if user.subscription:
            attended_sessions = GymSession.objects.filter(
                member=user, subscription=user.subscription)
            list_count = user.plan.sessions - attended_sessions.count()
            list_count = 0 if list_count < 0 else list_count

        add_subscription_form = AddSubscriptionForm(request=self.request)

        context = {
            'user': user,
            'attended_sessions': attended_sessions,
            'list_count': list_count,
            'add_subscription_form': add_subscription_form,
            'now': timezone.now(),
            'form': UserUpdateForm(instance=user)
        }

        return render(request, 'users/member.html', context)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserUpdateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            print('saved')
            return redirect('user-details', pk=pk)
        print(form.errors)
        attended_sessions = GymSession.objects.filter(
            member=user, subscription=user.subscription)
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
        return render(request, 'users/member.html', context)


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
def is_user_registered(request, tg_id):
    try:
        user = User.objects.get(telegram_id=tg_id)
        return Response({"user": user.first_name}, status=200)
    except User.DoesNotExist:
        return Response({"user": "not found"}, status=404)


@api_view(['POST'])
def register_new_user(request):
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


@api_view(['GET'])
def my_subscription(request, tg_id):
    try:
        subscription = User.objects.get(telegram_id=tg_id).subscription
        return Response({"plan": subscription.plan.name,
                         "start_date": subscription.start_date.strftime("%d-%m-%Y"),
                         "end_date": subscription.end_date.strftime("%d-%m-%Y"),
                         "left_sessions": subscription.left_sessions,
                         "used_sessions": subscription.used_sessions}, status=200)
    except:
        return Response({"msg": "Абонемент не найден"}, status=404)
