from django.urls import path
from . import views


app_name = 'gallery'
urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:image_id>', views.detail, name='detail'),
    path('<uuid:image_id>/download', views.download_image, name='download')
]
