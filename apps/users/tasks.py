import os
import qrcode
import random
from django.utils import timezone
from celery import shared_task
from django.core.files import File

from apps.users.models import Access, User


@shared_task()
def generate_and_save_access(user_id):
    user = User.objects.get(id=user_id)
    gym_code = user.gym.code if user.gym else "NN"
    code = gym_code + str(random.randint(10000, 99999))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data({"access_code": code})
    qr.make(fit=True)
    qr_dir = f"media/access_qr/{user.gym.name}/"
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)
    qr_code_name = f"{qr_dir}{code}.png"
    img = qr.make_image(fill_color="white", back_color="black")
    img.save(qr_code_name)
    access = Access.objects.create(
        code=code, gym=user.gym, user=user, image=File(open(qr_code_name, 'rb')))
    print(access)
    access.save()
