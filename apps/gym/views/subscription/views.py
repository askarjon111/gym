from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.common.choices import STATUS_CHOICES
from apps.gym.forms import AddSubscriptionForm


from apps.gym.models import Subscription
from apps.users.models import User
from apps.users.permissions import gym_manager_required


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
