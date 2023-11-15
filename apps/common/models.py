from django.db import models

from apps.common.utils import get_uploaded_file_type, user_upload_path


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class File(BaseModel):
    file = models.FileField(upload_to=user_upload_path, blank=True, null=True)

    def get_file_type(self):
        return get_uploaded_file_type(self.file)
