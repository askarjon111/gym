from celery import shared_task
import time
import base64
import telebot


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
