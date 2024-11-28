from apps.controls.models import Gym
from apps.users.models import User
from apps.users.utils import get_user_access
from .serializers import AccessSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class AccessByUserView(APIView):
    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).last()
        gym_id =  request.GET.get('gym_id')
        gym = Gym.objects.filter(id=gym_id).last()
        if not user or not gym:
            return Response({'error': 'User not found'}, 404)
        access = get_user_access(user, gym)
        print(access)
        return Response({'access': AccessSerializer(access).data})
