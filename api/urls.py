from django.urls import path
from .views import get_photos, create_photo, photo_detail, get_locations, create_location, location_detail, get_photoshoot, create_photoshoot, photoshoot_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('photo/', get_photos, name='photo_detail'),
    path('photo/create/', create_photo, name='create_photo'),
    path('photo/<int:pk>', photo_detail, name='photo_detail'),
    path('location/', get_locations, name='get_locations'),
    path('location/create/', create_location, name='create_location'),
    path('location/<int:pk>', location_detail, name='location_detail'),
    path('photoshoot/', get_photoshoot, name='get_photoshoot'),
    path('photoshoot/create/', create_photoshoot, name='create_photoshoot'),
    path('photoshoot/<int:pk>', photoshoot_detail, name='photoshoot_detail'),
]

# Only serve media files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)