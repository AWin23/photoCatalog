from django.urls import path
from .views import (
    get_photos, create_photo, photo_detail, get_locations,
    create_location, location_detail, get_photoshoot,
    create_photoshoot, photoshoot_detail, serve_photo_by_id
)
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('photo/', get_photos, name='photo_detail'),
    path('photo/create/', create_photo, name='create_photo'),
    path('photo/<int:pk>', photo_detail, name='photo_detail'),
    path('location/', get_locations, name='get_locations'),
    path('location/create/', create_location, name='create_location'),
    path('location/<int:pk>', location_detail, name='location_detail'),
    path('photoshoots/', get_photoshoot, name='get_photoshoot'),
    path('photoshoots/create/', create_photoshoot, name='create_photoshoot'),
    path('photoshoots/<int:pk>', photoshoot_detail, name='photoshoot_detail'),
    path("media/uploads", serve_photo_by_id, name="serve_photo_by_id"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
