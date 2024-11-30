from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView
from apps.gym.forms import AddNewGymEquipmentForm


from apps.gym.models import GymEquipment
from apps.users.permissions import gym_manager_required


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


@gym_manager_required(login_url='login')
def remove_equipment(request, pk):
    equipment = get_object_or_404(GymEquipment, id=pk)
    equipment.delete()
    return redirect('equipment')
