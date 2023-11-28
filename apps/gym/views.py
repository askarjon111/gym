from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.gym.models import GymSession
from apps.users.models import User


def home(request):
    return render(request, 'home.html')


@api_view(['POST'])
def create_session_view(request):
    member_id = request.POST.get('member_id')
    member = User.objects.filter(id=member_id).first()
    if member:
        GymSession.objects.create(member=member)


    return Response({"status": "ok"})