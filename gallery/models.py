from django.db import models


class Picture(models.Model):
    image_path = models.ImageField(upload_to='images/%Y/%m')
    description = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
