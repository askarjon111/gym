
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers

from apps.users.models import User
from apps.gym.models import GymSession


@api_view(['GET'])
def my_sessions_view(request, tg_id):
    try:
        subscription = User.objects.get(telegram_id=tg_id).subscription
        if subscription:
            sessions = GymSession.objects.filter(
                subscription=subscription)[:10]
            data = serializers.serialize('json', sessions)
            print(data)
        return Response({"sessions": data}, status=200)
    except Exception as e:
        return Response({"msg": f"Абонемент не найден {e}"}, status=404)


__all__ = ['my_sessions_view']
