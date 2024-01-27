from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
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
            instance = form.save()
            user = User.objects.get(phone_number=instance.phone_number)
            plan = Plan.objects.get(id=form.data['plan'])
            subs = Subscription.objects.create(member=user,
                                               plan=plan,
                                               start_date=form.data['start_date'],
                                               end_date=form.data['end_date'],
                                               status=Subscription.STATUS_CHOICES[0][0])
        else:
            print(form.errors)
        return redirect('users')

    def get(self, request):
        return render(request, self.template_name, {'form': UserCreateForm(request=request)})


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class MembersListView(LoginRequiredMixin, View):
    template_name = 'users/members.html'
    context_object_name = 'members'
    paginate_by = 20
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        gym = self.request.user.gym
        if gym:
            members = Gym.objects.get_users(gym.id).order_by('-id')
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
class UserDetail(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = User
    template_name = 'users/member.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs['object'].subscription:
            context['attended_sessions'] = GymSession.objects.filter(
                member=kwargs['object'], subscription=kwargs['object'].subscription)
            context['list'] = kwargs['object'].plan.sessions - \
                context['attended_sessions'].count()
            context['list'] = 0 if context['list'] < 0 else context['list']
        context['add_subscription_form'] = AddSubscriptionForm(
            request=self.request)
        context['now'] = timezone.now()
        return context


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class UserUpdateView(LoginRequiredMixin, FormView):
    login_url = 'login'
    template_name = 'users/member.html'
    form_class = UserUpdateForm

    def get_initial(self):
        return {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'region': self.request.user.region,
            'city': self.request.user.city,
            'location': self.request.user.location,
            'description': self.request.user.description,
            'telegram_id': self.request.user.telegram_id,
        }

    def form_valid(self, form):
        user = User.objects.get(pk=form.cleaned_data['user_id'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.phone_number = form.cleaned_data['phone_number']
        try:
            user.save()
            return redirect('home')
        except Exception as e:
            print(f"{e}")
            messages.add_message(self.request, messages.WARNING,
                                 "Xato")
            return redirect('user-details', form.cleaned_data['user_id'])


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
