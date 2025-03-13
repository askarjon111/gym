from rest_framework.response import Response
from rest_framework.decorators import api_view

from apps.gym.models import Subscription
from apps.users.models import User


@api_view(['GET'])
def my_subscription_view(request, tg_id):
    try:
        user = User.objects.get(telegram_id=tg_id).subscription
        subscription = Subscription.objects.get(user=user)
        return Response({"plan": subscription.plan.name,
                         "start_date": subscription.start_date.strftime("%d-%m-%Y"),
                         "end_date": subscription.end_date.strftime("%d-%m-%Y"),
                         "left_sessions": subscription.left_sessions,
                         "used_sessions": subscription.used_sessions}, status=200)
    except Subscription.DoesNotExist:
        return Response({"msg": "Абонемент не найден"}, status=404)


__all__ = ['my_subscription_view']
