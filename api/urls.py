from django.urls import path
from .views import get_photos, create_photo, photo_detail

urlpatterns = [
    path('photo/', get_photos, name='get_photos'),
    path('photo/create/', create_photo, name='create_photo'),
    path('photo/<int:pk>', photo_detail, name='photo_detail')
]