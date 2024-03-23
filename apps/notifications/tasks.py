from django.utils import timezone
from celery import shared_task
import time
import base64
import telebot

from apps.notifications.models import Notification


@shared_task()
def call_send_message():
    notifications = Notification.objects.filter(send_at__lte=timezone.now(),
                                                sent=False,
                                                is_draft=False,
                                                receiver__isnull=False)

    if notifications:
        for notification in notifications:
            notification.send()
            notification.sent = True
            notification.save()


@shared_task
def send_message(title, receiver_list, token, message=None, photo=None, video=None):
    bot = telebot.TeleBot(token)
    message = f"<b>{title}</b>\n{message if message else ''}"
    if video is not None:
        for telegram_id in receiver_list:
            try:
                bot.send_video(telegram_id, base64.b64decode(
                    video), caption=message, parse_mode='HTML')
                time.sleep(1)
            except Exception as e:
                print(e)
    elif photo is not None:
        for telegram_id in receiver_list:
            try:
                bot.send_photo(telegram_id, base64.b64decode(
                    photo), caption=message, parse_mode='HTML')
                time.sleep(1)
            except Exception as e:
                print(e)
    else:
        for telegram_id in receiver_list:
            try:
                bot.send_message(telegram_id, message, parse_mode='HTML')
                time.sleep(1)
            except Exception as e:
                print(e)

    return "OK"
