import uuid
from uuid import UUID
from django.http import QueryDict  # Import QueryDict to fix NameError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict
from .models import Photo, Location, Photoshoot, PhotoshootPhotoJunction
from .serializer import PhotoSerializer, LocationSerializer, PhotoshootSerializer, PhotoshootPhotoJunctionSerializer


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

    data = request.data.dict()  # Convert to a mutable dictionary
    print(f"Initial payload: {data}")

    # Validate or generate PhotoGUID
    if 'PhotoGUID' not in data:
        print("PhotoGUID missing in payload. Generating a new UUID.")
        data['PhotoGUID'] = str(uuid.uuid4())
    else:
        print(f"Received PhotoGUID: {data['PhotoGUID']}")
        if not is_valid_uuid(data['PhotoGUID']):
            print(f"PhotoGUID {data['PhotoGUID']} is invalid. Generating a new UUID.")
            data['PhotoGUID'] = str(uuid.uuid4())

    try:
        data['PhotoGUID'] = uuid.UUID(data['PhotoGUID'])
        print(f"Converted PhotoGUID to UUID object: {data['PhotoGUID']}")
    except ValueError as e:
        print(f"Failed to convert PhotoGUID to UUID: {e}")
        return Response({'error': f'Invalid UUID: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    # Handle the image file separately
    if 'image' in request.FILES:
        image_file = request.FILES['image']
        data['FileName'] = image_file.name
        data['ImagePath'] = image_file.name  # Adjust based on storage needs
    else:
        print("No image file found in request.")
        return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Serialize and save
    serializer = PhotoSerializer(data=data)  
    if serializer.is_valid():
        serializer.save()
        print(f"Photo saved successfully: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    print(f"Serializer errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['POST'])
def create_location(request):
    # Make a mutable copy of the request data
    data = request.data.copy()
    
    print(f"Initial payload: {data}")

    # Serialize and save
    serializer = LocationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print(f"Location saved successfully: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print(f"Serializer errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get Photoshoot Endpoint
@api_view(['GET'])
def get_photoshoot(request):
    # Use select_related to optimize foreign key lookups (LocationId in Photoshoot)
    photoshoot = Photoshoot.objects.all().select_related('LocationId')
    
    # Serialize the data using PhotoshootSerializer
    serializer = PhotoshootSerializer(photoshoot, many=True)
    
    # Return the serialized data as a response
    return Response(serializer.data)

# Create a Photoshoot 
@api_view(['POST'])
def create_photoshoot(request):
    # Make a mutable copy of the request data
    data = request.data.copy()
    
    print(f"Initial payload: {data}")

    # Serialize and save
    serializer = PhotoshootSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print(f"Photoshoot saved successfully: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print(f"Serializer errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Photoshoot CRUD Operations 
@api_view(['GET', 'PUT', 'DELETE'])
def photoshoot_detail(request, pk):
    try:
        photoshoot_detail = Photoshoot.objects.get(pk=pk)
    except Photoshoot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # If we are trying to GET a specific Photoshoot
    if request.method == 'GET':
        serializer = PhotoshootSerializer(photoshoot_detail)
        return Response(serializer.data)
    
    # If we are trying to update Location
    elif request.method == 'PUT':
        serializer = PhotoshootSerializer(photoshoot_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        photoshoot_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

