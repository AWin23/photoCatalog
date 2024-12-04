from django.urls import path
from .views import get_photos, create_photo, photo_detail, get_locations, create_location, location_detail

urlpatterns = [
    path('photo/', get_photos, name='photo_detail'),
    path('photo/create/', create_photo, name='create_photo'),
    path('photo/<int:pk>', photo_detail, name='photo_detail'),
    path('location/', get_locations, name='get_locations'),
    path('location/create/', create_location, name='create_location'),
    path('location/<int:pk>', location_detail, name='location_detail'),
]