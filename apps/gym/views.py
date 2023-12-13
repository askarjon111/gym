from datetime import timedelta
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.gym.forms import AddSubscriptionForm


from apps.gym.models import GymSession, Plan, Subscription
from apps.users.models import User


@login_required(login_url = 'login')
def home(request):
    users = User.objects.all()
    active_subscriptions = Subscription.objects.filter(end_date__gte=timezone.now(),
                                                       status=Subscription.STATUS_CHOICES[0][0])
    print(active_subscriptions)
    active_members = [subscription.member for subscription in active_subscriptions]
    new_members = users.filter(created_at__gte=timezone.now() - timedelta(days=7)).count()
    return render(request, 'home.html', context={"users": users.count(),
                                                 "active_members": len(active_members),
                                                 "new_members": new_members})


@login_required(login_url = 'login')
@api_view(['POST'])
def create_session_view(request):
    member_id = request.POST.get('member_id')
    member = User.objects.filter(id=member_id).first()
    if member:
        GymSession.objects.create(member=member)


    return Response({"status": "ok"})


class PlansView(View):
    template_name = 'gym/plans.html'

    def get(self, request):
        plans = Plan.objects.all()
        return render(request, self.template_name, {'plans': plans})


class AddSubscriptionView(View):
    model = Subscription
    template_name = 'users/member.html'

    def post(self, request):
        form = AddSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print('error')
            print(form.errors)
        return redirect('user-details', form.data['member'])
