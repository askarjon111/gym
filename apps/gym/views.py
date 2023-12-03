from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.gym.models import GymSession, Subscription
from apps.users.models import User


def home(request):
    users = User.objects.all()
    active_subscriptions = Subscription.objects.filter(end_date__gte=timezone.now())
    active_members = [subscription.member for subscription in active_subscriptions]
    new_members = users.filter(created_at__gte=timezone.now() - timedelta(days=7)).count()
    return render(request, 'home.html', context={"users": users.count(),
                                                 "active_members": len(active_members),
                                                 "new_members": new_members})

@api_view(['POST'])
def create_session_view(request):
    member_id = request.POST.get('member_id')
    member = User.objects.filter(id=member_id).first()
    if member:
        GymSession.objects.create(member=member)


    return Response({"status": "ok"})