from django.contrib import admin
from .models import Picture


class PictureAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("description",)}


admin.site.register(Picture, PictureAdmin)
