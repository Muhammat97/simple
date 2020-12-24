import uuid
from django.db import models


class Picture(models.Model):
    picture_uuid = models.UUIDField(default=uuid.uuid4(), editable=False, unique=True)
    image_path = models.ImageField(upload_to='images/%Y/%m')
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
