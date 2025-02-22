from django.db import models
from django.contrib.auth.models import User  # Assuming Django's built-in User model
import uuid  # For generating UUIDs

    # Class for Photo
class Photo(models.Model):
    PhotoID = models.AutoField(primary_key=True)  # Identity column as primary key
    #PhotoGUID = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)  # Avoid null=True for UUID
    FileName = models.CharField(max_length=256, null=True, blank=True)  # Matches `nvarchar(256)`
    TimeStamp = models.DateTimeField(null=True, blank=True)  # Matches `datetime2(7)`
    ImagePath = models.ImageField(upload_to='uploads/', null=True, blank=True)  # Store image field


    class Meta:
        db_table = "Photo"  # Ensure the table name is consistent

    def __str__(self):
        return f"{self.id} - {self.TimeStamp}"
    
    # Class for Location
class Location(models.Model):
    LocationId = models.AutoField(primary_key=True)
    LocationName = models.CharField(max_length=256, null=True, blank=True)
    Address = models.CharField(max_length=512, null=True, blank=True)
    Latitude = models.FloatField(null=True, blank=True)
    Longitude = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "Location"

    def __str__(self):
        return f"{self.LocationId} - {self.LocationName}"


    
    # Class for Photoshoot
class Photoshoot(models.Model):
    PhotoshootId = models.AutoField(primary_key=True) # Identify column as Primary key
    LocationId = models.ForeignKey(Location, on_delete=models.CASCADE, db_column='LocationId')
    Date = models.DateTimeField(null=True, blank=True)  # Matches `datetime2(7)`
    
    class Meta:
        db_table = "Photoshoot" # Ensure the table name matches
        
    def __str__(self):
        return f"{self.PhotoshootId} - {self.Date}"
    
    # Class for PhotoshootPhotoJunction
class PhotoshootPhotoJunction(models.Model):
    PhotoID = models.ForeignKey(Photo, on_delete=models.CASCADE, db_column='PhotoID')
    PhotoshootId = models.ForeignKey(Photoshoot, on_delete=models.CASCADE, db_column='PhotoshootID')
    
    class Meta: 
        db_table = "PhotoshootPhotoJunction"
        
    def __str__(self):
        return f"{self.PhotoID} - {self.PhotoshootId}"

