from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from apps.notifications.forms import NotificationForm
from apps.notifications.models import Notification
from apps.users.permissions import gym_manager_required


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class NotificationsListView(LoginRequiredMixin, View):
    template_name = 'notifications/notifications.html'
    context_object_name = 'objects'
    paginate_by = 20
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        gym = self.request.user.gym
        if gym:
            notifications = Notification.objects.filter(gym=gym)

        if query:
            notifications = notifications.filter(
                Q(title__icontains=query) | Q(body__icontains=query) | Q(receiver__phone_number__icontains=query)
            )
        paginator = Paginator(notifications, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            notifications = paginator.page(page)
        except PageNotAnInteger:
            notifications = paginator.page(1)
        except EmptyPage:
            notifications = paginator.page(paginator.num_pages)
        form = NotificationForm(request.POST, request=request)
        return render(request, self.template_name, {'objects': notifications, 'form': form})

    def post(self, request, *args, **kwargs):
        form = NotificationForm(request.POST, request=request)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.gym = request.user.gym
            notification.save()
            return redirect('notifications')
        else:
            print(form.errors)
            notifications = Notification.objects.filter(gym=request.user.gym)
            context = {'objects': notifications, 'form': form}
            return render(request, self.template_name, context)


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class NotificationDetailView(LoginRequiredMixin, View):
    template_name = 'notifications/single_notification.html'
    login_url = 'login'

    def get(self, request, pk, *args, **kwargs):
        gym = self.request.user.gym
        if gym:
            notification = Notification.objects.get(pk=pk)

        form = NotificationForm(request.POST, request=request, instance=notification)
        return render(request, self.template_name, {'notification': notification, 'form': form})

    def post(self, request, *args, **kwargs):
        form = NotificationForm(request.POST, request=request)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.gym = request.user.gym
            notification.save()
            return redirect('notifications')
        else:
            print(form.errors)
            notifications = Notification.objects.filter(gym=request.user.gym)
            context = {'objects': notifications, 'form': form}
            return render(request, self.template_name, context)
