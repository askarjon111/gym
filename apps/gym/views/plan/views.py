from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.gym.forms import AddNewPlanForm


from apps.gym.models import Plan
from apps.users.permissions import gym_manager_required
from project.settings import ERROR_PATTERN

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
