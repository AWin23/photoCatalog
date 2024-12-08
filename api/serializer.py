from rest_framework import serializers
from .models import Photo, Location, Photoshoot

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
    # This will ensure that the location field is serialized properly
    LocationId = LocationSerializer(read_only=True)

    class Meta:
        model = Photoshoot
        fields = '__all__'
        
    def validate_LocationId(self, value):
        # Ensure LocationId exists in the Location table
        if not Location.objects.filter(LocationId=value).exists():
            raise serializers.ValidationError("Invalid LocationId")
        return value

