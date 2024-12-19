from rest_framework import serializers
from .models import Photo, Location, Photoshoot, PhotoshootPhotoJunction

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ['PhotoGUID']  # Prevent manual input
        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        
class PhotoshootSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photoshoot
        fields = '__all__'
        
class PhotoshootPhotoJunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoshootPhotoJunction
        fields = '__all__'
        


