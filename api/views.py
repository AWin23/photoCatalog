import uuid
from uuid import UUID
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict
from .models import Photo
from .serializer import PhotoSerializer

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
    
# Post a new Photo
@api_view(['POST'])
def create_photo(request):
    # Make a mutable copy of the request data
    data = request.data.copy()
    
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
        else:
            print(f"PhotoGUID {data['PhotoGUID']} is valid.")

    # Convert PhotoGUID to a UUID object explicitly
    try:
        data['PhotoGUID'] = uuid.UUID(data['PhotoGUID'])  # Ensure it's a UUID object
        print(f"Converted PhotoGUID to UUID object: {data['PhotoGUID']}")
    except ValueError as e:
        error_message = f"Failed to convert PhotoGUID to UUID: {e}"
        print(error_message)
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

    # Serialize and save
    serializer = PhotoSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print(f"Photo saved successfully: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print(f"Serializer errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# CRUD Operations
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
