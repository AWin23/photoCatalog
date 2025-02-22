from rest_framework import serializers
from .models import Photo, Location, Photoshoot, PhotoshootPhotoJunction

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ['PhotoGUID']  # Prevent manual input
        
class LocationSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='LocationName', required=False)
    address = serializers.CharField(source='Address', required=False)
    latitude = serializers.FloatField(source='Latitude', required=False)
    longitude = serializers.FloatField(source='Longitude', required=False)

    class Meta:
        model = Location
        fields = ['LocationId', 'location_name', 'address', 'latitude', 'longitude']

        
class PhotoshootSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photoshoot
        fields = '__all__'
        
class PhotoshootPhotoJunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoshootPhotoJunction
        fields = '__all__'
        


