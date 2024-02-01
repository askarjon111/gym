from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.controls.models import Gym
from apps.gym.forms import AddNewPlanForm, AddSubscriptionForm


from apps.gym.models import GymSession, Plan, Subscription
from apps.users.models import User
from apps.users.permissions import gym_manager_required


@gym_manager_required(login_url='login')
def home(request):
    gym = request.user.gym
    if gym:
        users = Gym.objects.get_members(gym.id)

    active_subscriptions = Subscription.objects.filter(end_date__gte=timezone.now(),
                                                       status=Subscription.STATUS_CHOICES[0][0],
                                                       plan__gym=gym)
    active_members = [
        subscription.member for subscription in active_subscriptions]
    new_members = users.filter(
        created_at__gte=timezone.now() - timedelta(days=7)).count()
    return render(request, 'home.html', context={"users": users.count(),
                                                 "active_members": len(active_members),
                                                 "new_members": new_members})


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class PlansView(View):
    template_name = 'gym/plans.html'
    form = AddNewPlanForm

    def get(self, request):
        gym = self.request.user.gym
        if gym:
            plans = gym.plans
        return render(request, self.template_name, {'plans': plans, 'form': AddNewPlanForm})


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class AddNewPlanView(View):
    model = Plan
    template_name = 'users/plans.html'

    def post(self, request):
        form = AddNewPlanForm(request.POST)
        if form.is_valid():
            form.save(gym=self.request.user.gym)
        else:
            print(form.errors)
        return redirect('plans')


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class AddSubscriptionView(View):
    model = Subscription
    template_name = 'users/member.html'

    def post(self, request):
        form = AddSubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.status = Subscription.STATUS_CHOICES[0][0]
            subscription.save()
        else:
            print(form.errors)
        return redirect('user-details', form.data['member'])


class DeletePlanView(View):
    template_name = 'plans.html'

    def get(self, request, plan_id):
        plan = get_object_or_404(Plan, id=plan_id)
        return render(request, self.template_name, {'plan': plan})

    def post(self, request, pk):
        plan = get_object_or_404(Plan, id=pk)
        plan.delete()
        return redirect('plans')
