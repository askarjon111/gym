from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.common.choices import STATUS_CHOICES
from apps.controls.models import Gym
from apps.gym.forms import AddNewGymEquipmentForm, AddNewPlanForm, AddSubscriptionForm


from apps.gym.models import GymEquipment, GymSession, Plan, Subscription
from apps.users.models import User
from apps.users.permissions import gym_manager_required
from project.settings import ERROR_PATTERN


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
class UpdatePlanView(View):
    template_name = 'gym/plan_update.html'

    def get(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk, gym=request.user.gym)
        form = AddNewPlanForm(instance=plan)
        return render(request, self.template_name, {'form': form, 'plan': plan})

    def post(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        form = AddNewPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, "План успешно обновлен!")
            return redirect('plans')
        else:
            errors = ERROR_PATTERN.search(str(form.errors)).group(1)
            messages.add_message(request, messages.WARNING, f"Ошибка: {errors}")
            return render(request, self.template_name, {'form': form, 'plan': plan})


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class AddNewPlanView(View):
    model = Plan
    template_name = 'users/plans.html'

    def post(self, request):
        form = AddNewPlanForm(request.POST, gym=self.request.user.gym)
        if form.is_valid():
            form.save()
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


    def get(self, request, pk):
        user = User.objects.get(id=pk)
        return render(request, 'users/add_subscription.html',
                      {'user': user,
                       'form': AddSubscriptionForm(request=request),
                       'page_title': 'Абонемент',
                       'next_step': 'Сохранить'})


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


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class EquipmentView(View):
    template_name = 'gym/equipment.html'
    form = AddNewGymEquipmentForm

    def get(self, request):
        gym = self.request.user.gym
        if gym:
            equipment = gym.gymequipment_set.all()
        return render(request, self.template_name, {'equipment': equipment, 'form': self.form})


@method_decorator(gym_manager_required(login_url='login'), name='dispatch')
class AddNewGymEquipmentView(CreateView):
    model = GymEquipment
    template_name = 'users/equipment.html'

    def post(self, request):
        form = AddNewGymEquipmentForm(request.POST, request.FILES, gym=self.request.user.gym)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect('equipment')
