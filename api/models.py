from django.db import models
import uuid  # For generating UUIDs

    # Class for Photo
class Photo(models.Model):
    PhotoID = models.AutoField(primary_key=True)  # Identity column as primary key
    #PhotoGUID = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)  # Avoid null=True for UUID
    FileName = models.CharField(max_length=256, null=True, blank=True)  # Matches `nvarchar(256)`
    TimeStamp = models.DateTimeField(null=True, blank=True)  # Matches `datetime2(7)`

    class Meta:
        db_table = "Photo"  # Ensure the table name is consistent

    def __str__(self):
        return f"{self.id} - {self.TimeStamp}"
    
    # Class for Location
class Location(models.Model):
    LocationId = models.AutoField(primary_key=True)
    LocationName = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "Location"  # Ensure the table name is consistent

    def __str__(self):
        return f"{self.LocationId} - {self.LocationName}"
