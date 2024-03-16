from django.db import models
from apps.common.models import BaseModel
from apps.controls.models import Gym
from apps.users.models import User


def content_file_name(instance, filename):
    return '/'.join(['notification_files', instance.gym.name, filename])


class Notification(BaseModel):
    TYPE_CHOICES = (('sms', 'sms'), ('telegram', 'telegram'),)

    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=content_file_name, blank=True, null=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    send_at = models.DateTimeField(blank=True, null=True)
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES[1][1])
    sent = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)


    def send(self):
        from apps.notifications.tasks import send_message
        receiver = self.receiver.phone_number if self.type == self.TYPE_CHOICES[0][0] else self.receiver.telegram_id
        send_message.delay(self.title,
                           [receiver, ],
                           self.gym.telegram_bot_token,
                           message=self.body)

    class Meta:
        ordering = ['-id']