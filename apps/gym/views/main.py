from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.common.choices import STATUS_CHOICES
from apps.controls.models import Gym
from apps.gym.forms import AddNewPlanForm, AddSubscriptionForm


from apps.gym.models import GymSession, Plan, Subscription
from apps.users.models import User
from apps.users.permissions import gym_manager_required


@gym_manager_required(login_url='login')
def home(request):
    gym = request.user.gym
    notifications = gym.gymnotification_set.filter(
        status=STATUS_CHOICES[0][0]).order_by('-send_at')[:5]
    return render(request, 'home.html', context={"users": len(gym.members),
                                                 "active_members": len(gym.active_members),
                                                 "new_members": len(gym.new_members),
                                                 'notifications': notifications})


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class PlansView(View):
    template_name = 'gym/plans.html'
    form = AddNewPlanForm

    def get(self, request):
        gym = self.request.user.gym
        if gym:
            plans = gym.plans.order_by('-is_active')
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
            subscription.status = STATUS_CHOICES[0][0]
            subscription.save()
        else:
            print(form.errors)
        return redirect('user-details', form.data['member'])


class ArchivePlanView(View):
    template_name = 'plans.html'

    def get(self, request, plan_id):
        plan = get_object_or_404(Plan, id=plan_id)
        return render(request, self.template_name, {'plan': plan})

    def post(self, request, pk):
        plan = get_object_or_404(Plan, id=pk)
        plan.is_active = False
        plan.save()
        return redirect('plans')


@gym_manager_required(login_url='login')
@api_view(['GET'])
def get_plan_days(request, plan_id):
    try:
        plan = Plan.objects.get(pk=plan_id)
        days = plan.days
        return Response({'days': days})
    except Plan.DoesNotExist:
        return Response({'error': 'Plan not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


# @gym_manager_required(login_url='login')
@api_view(['POST'])
def cancel_subscription(request, sub_id):
    try:
        subscription = Subscription.objects.get(pk=sub_id)
        subscription.status = STATUS_CHOICES[1][0]
        subscription.save()
        return Response({'status': 'ok'}, status=200)
    except Subscription.DoesNotExist:
        return Response({'error': 'Subscription not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
