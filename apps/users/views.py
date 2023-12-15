from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView
from django.db.models import Q
from apps.gym.forms import AddSubscriptionForm

from apps.users.models import User
from apps.gym.models import GymSession, Plan, Subscription
from apps.users.forms import AttendanceForm, UserProfileForm


class CreateUser(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/add_user.html'
    login_url = 'login'


    def post(self, request):
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(phone_number=form.data['phone_number'])
            plan = Plan.objects.get(id=form.data['plan'])
            subs = Subscription.objects.create(member=user,
                                               plan=plan,
                                               start_date=form.data['start_date'],
                                               end_date=form.data['end_date'],
                                               status=Subscription.STATUS_CHOICES[0][0])
        else:
            print(form.errors)
        return redirect('users')


class MembersListView(LoginRequiredMixin, View):
    template_name = 'users/members.html'
    context_object_name = 'members'
    paginate_by = 5
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        members = User.objects.all().order_by('-id')
        now = timezone.now()

        if query:
            members = members.filter(
                Q(phone_number__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        form = AttendanceForm()
        return render(request, self.template_name, {'members': members,
                                                    'form': form,
                                                    'now': now,
                                                    'add_subscription_form': AddSubscriptionForm()})

    def post(self, request, *args, **kwargs):
        form = AttendanceForm(request.POST, request=request)
        if form.is_valid():
            form.save(start=timezone.now())
            return redirect('users')

        return render(request, self.template_name, {'members': User.objects.all().order_by('-id'), 'form': form})

class UserDetail(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = User
    template_name = 'users/member.html'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs['object'].subscription:
            context['attended_sessions'] = GymSession.objects.filter(member=kwargs['object'], subscription=kwargs['object'].subscription)
            context['list'] = kwargs['object'].plan.sessions - context['attended_sessions'].count()
        context['add_subscription_form'] = AddSubscriptionForm()
        context['now'] = timezone.now()
        return context


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()


    return render(request, 'users/login.html', {'form': form})


class LogOutView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        logout(request)
        return redirect(self.login_url)