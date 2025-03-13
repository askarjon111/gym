from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from apps.controls.models import Gym
from apps.gym.forms import AddSubscriptionForm

from apps.users.models import User
from apps.users.forms import AttendanceForm
from apps.users.permissions import gym_manager_required


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class MembersListView(LoginRequiredMixin, View):
    template_name = 'users/members.html'
    context_object_name = 'objects'
    paginate_by = 20
    login_url = 'login'

    def get_queryset(self):
        query = self.request.GET.get('q')
        gym = self.request.user.gym
        if gym:
            users = gym.users.filter(gyms=gym).prefetch_related('subscriptions', 'gyms').only('phone_number', 'subscriptions')
        if query:
            users = users.filter(
                Q(phone_number__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
        return users

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        users = self.get_queryset()
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
                Q(phone_number__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
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


__all__ = ['MembersListView', 'StaffListView']
