
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.common.choices import STATUS_CHOICES
from apps.controls.models import Gym
from apps.gym.forms import AddSubscriptionForm
from django.core import serializers

from apps.users.models import Lead, User, UserProfile
from apps.gym.models import GymSession, Subscription
from apps.users.forms import AttendanceForm, LeadForm, UserCreateForm, UserProfileUpdateForm, UserRegistrationForm, UserUpdateForm
from apps.users.permissions import gym_manager_required
from apps.users.tasks import generate_and_save_access
from project.settings import ERROR_PATTERN


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class CreateUser(View):
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
        except:
            messages.add_message(self.request, messages.WARNING,
                                 f"Произошла ошибка, свяжитесь с администратором.")
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


@api_view(['GET'])
def my_sessions(request, tg_id):
    try:
        subscription = User.objects.get(telegram_id=tg_id).subscription
        if subscription:
            sessions = GymSession.objects.filter(
                subscription=subscription)[:10]
            data = serializers.serialize('json', sessions)
            print(data)
        return Response({"sessions": data}, status=200)
    except:
        return Response({"msg": "Абонемент не найден"}, status=404)


@gym_manager_required(login_url='login')
def leads(request):
    leads = Lead.objects.filter(operator=request.user)

    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.instance.operator = request.user
            form.save()
            return redirect('leads')
        else:
            errors = ERROR_PATTERN.search(str(form.errors)).group(1)
            messages.add_message(
                request, messages.WARNING, f"Ошибка: {errors}")
            return redirect('leads')
    else:
        query = request.GET.get('q', None)
        if query:
            leads = leads.filter(Q(first_name__contains=query) | Q(last_name__contains=query) |
                                 Q(phone_number__contains=query))
        paginator = Paginator(leads, 20)
        page = request.GET.get('page')

        try:
            leads = paginator.page(page)
        except PageNotAnInteger:
            leads = paginator.page(1)
        except EmptyPage:
            leads = paginator.page(paginator.num_pages)
        form = LeadForm()
    return render(request, 'users/leads.html', {'form': form, 'objects': leads})


@gym_manager_required(login_url='login')
def lead_edit(request, pk):
    lead = Lead.objects.get(pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
    else:
        form = LeadForm(instance=lead)
    return render(request, 'users/lead_edit.html', {'form': form, 'lead': lead})


@gym_manager_required(login_url='login')
def lead_delete(request, pk):
    lead = Lead.objects.get(pk=pk)
    if request.method == 'POST':
        lead.delete()
        return redirect('leads')
    return render(request, 'lead_delete.html', {'lead': lead})


def activate_lead(request):
    if request.method == 'POST':
        lead = Lead.objects.filter(id=request.POST.get('member')).first()
        user, _ = User.objects.update_or_create(phone_number=lead.phone_number,
                                                defaults={'first_name': lead.first_name, 'last_name': lead.last_name})
        user.gyms.add(request.user.gym)
        user.save()
        lead.status = Lead.STATUS_CHOICES[2][0]
        lead.save()
        return redirect('user-details', pk=user.pk)


@gym_manager_required(login_url='login')
def canceled_lead(request):
    if request.method == 'POST':
        lead = Lead.objects.filter(id=request.POST.get('member')).first()
        lead.status = Lead.STATUS_CHOICES[3][0]
        lead.save()
        return redirect('leads')
