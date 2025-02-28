import uuid
from uuid import UUID
import requests
from django.http import QueryDict  # Import QueryDict to fix NameError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict
from .models import Photo, Location, Photoshoot, PhotoshootPhotoJunction
from .serializer import PhotoSerializer, LocationSerializer, PhotoshootSerializer, PhotoshootPhotoJunctionSerializer
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
from dotenv import load_dotenv

# Load the .env file from the parent directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', 'photocatalog' , '.env'))

# Access your API key
GOOGLE_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
print(f"API Key: {GOOGLE_API_KEY}")  # Debug line to check the value



# Get Photo Endpoint
@api_view(['GET'])
def get_photos(request):
    photos = Photo.objects.all()
    serializer = PhotoSerializer(photos, many=True)
    return Response(serializer.data)  # Return the actual data from the database


def is_valid_uuid(val):
    try:
        UUID(val, version=4)
        return True
    except ValueError:
        return False
    
    
@api_view(['POST'])
@parser_classes([MultiPartParser])
def create_photo(request):
    print(f"Request data type: {type(request.data)}")
    print(f"Initial payload: {request.data}")

    # Extract form data without deepcopy
    data = request.data.dict()  # ✅ Prevents deepcopy issue

    # Validate or generate PhotoGUID
    if 'PhotoGUID' not in data:
        print("PhotoGUID missing in payload. Generating a new UUID.")
        data['PhotoGUID'] = str(uuid.uuid4())
    elif not is_valid_uuid(data['PhotoGUID']):
        print(f"PhotoGUID {data['PhotoGUID']} is invalid. Generating a new UUID.")
        data['PhotoGUID'] = str(uuid.uuid4())

    try:
        data['PhotoGUID'] = uuid.UUID(data['PhotoGUID'])
        print(f"Converted PhotoGUID to UUID object: {data['PhotoGUID']}")
    except ValueError as e:
        return Response({'error': f'Invalid UUID: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    # Handle image file separately
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

    data['FileName'] = image_file.name
    data['ImagePath'] = image_file  # Keep actual file object

    # Serialize and save
    serializer = PhotoSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def serve_photo_by_id(request, photo_id):
    try:
        # Retrieve the specific photo by its ID
        photo = Photo.objects.get(PhotoID=photo_id)
        
        # Ensure `photo.ImagePath` is a string and construct the full path
        file_path = os.path.join(settings.MEDIA_ROOT, str(photo.ImagePath))

        # Debugging statement to see what path is being accessed
        print(f"Serving image from: {file_path}")

        if os.path.exists(file_path):
            return FileResponse(open(file_path, "rb"), content_type="image/jpeg")  # Adjust MIME type if needed

        return HttpResponse("File not found", status=404)
    
    except Photo.DoesNotExist:
        return HttpResponse("Photo not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


# Photo CRUD Operations
@api_view(['GET', 'PUT', 'DELETE'])
def photo_detail(request, pk):
    try:
        photo = Photo.objects.get(pk=pk)
    except Photo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # If we are trying to GET a specific PhotoID
    if request.method == 'GET':
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)
    
    # If we are trying to update
    elif request.method == 'PUT':
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Get Location Endpoint
@api_view(['GET'])
def get_locations(request):
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)  # Return the actual data from the database

# Location CRUD Operations 
@api_view(['GET', 'PUT', 'DELETE'])
def location_detail(request, pk):
    try:
        location = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # If we are trying to GET a specific Location
    if request.method == 'GET':
        serializer = LocationSerializer(location)
        return Response(serializer.data)
    
    # If we are trying to update Location
    elif request.method == 'PUT':
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_lat_lon_from_address(address):
    """Fetch latitude and longitude using Google Maps Geocoding API"""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        latitude, longitude = location["lat"], location["lng"]
        
        print("Geocoding result:", latitude, longitude)  # ✅ Now this works correctly
        
        return latitude, longitude
    
    print("❌ Geocoding API failed:", data)  # 🔍 Log the full response to debug
    return None, None  # Return None if the API fails

@api_view(['POST'])
def create_location(request):
    print("Incoming request data:", request.data)  # Debugging
    
    data = request.data.copy()
    address = data.get("address", "").strip()

    if not address:
        print("❌ Address is missing!")
        return Response({"error": "Address is required"}, status=status.HTTP_400_BAD_REQUEST)

    latitude, longitude = get_lat_lon_from_address(address)
    if latitude is None or longitude is None:
        print("❌ Failed to fetch lat/lng from address!")
        return Response({"error": "Failed to fetch latitude/longitude"}, status=status.HTTP_400_BAD_REQUEST)

    data["latitude"] = latitude
    data["longitude"] = longitude

    print("✅ Data before serializer:", data)  # 🔍 Check if data is correctly formatted before the serializer

    serializer = LocationSerializer(data=data)
    print("✅ Serializer instantiated")

    if serializer.is_valid():
        print("✅ Validated data before saving:", serializer.validated_data)
        location = serializer.save()
        print(f"✅ Location saved: {location}")  # Debugging
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print("❌ Validation Errors:", serializer.errors)  # 🔥 Log the actual error
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Get Photoshoot Endpoint or # GET /api/photoshoots?locationID=123
@api_view(['GET'])
def get_photoshoot(request):
    location_id = request.GET.get('locationId')  # Match the parameter name exactly

    if location_id:
        photoshoots = Photoshoot.objects.filter(LocationId=location_id).values("PhotoshootId", "Date", "LocationId")  # Ensure LocationId is included for clarity
    else:
        photoshoots = Photoshoot.objects.all().values("PhotoshootId", "Date", "LocationId")

    return Response(list(photoshoots))  # Convert QuerySet to list to avoid potential serialization issues



# POST /api/photoshoot/create
@api_view(['POST'])
def create_photoshoot(request):
    print("Received Data:", request.data)  # Debugging line
    
    data = request.data
    location_id = data.get('LocationId')
    date = data.get('Date')

    if not location_id or not date:
        return Response({"error": "LocationId and Date are required"}, status=status.HTTP_400_BAD_REQUEST)

    location = get_object_or_404(Location, pk=location_id)

    new_photoshoot = Photoshoot(LocationId=location, Date=date)
    new_photoshoot.save()

    return Response({"message": "Photoshoot scheduled successfully!", "PhotoshootId": new_photoshoot.PhotoshootId}, status=status.HTTP_201_CREATED)

# Photoshoot CRUD Operations 
@api_view(['GET', 'PUT', 'DELETE'])
def photoshoot_detail(request, pk):
    try:
        photoshoot = Photoshoot.objects.get(pk=pk)
    except Photoshoot.DoesNotExist:
        return Response({"error": "Photoshoot not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PhotoshootSerializer(photoshoot)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PhotoshootSerializer(photoshoot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        photoshoot.delete()
        return Response({"message": "Photoshoot deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


