from django.db import models
from django.core.exceptions import ValidationError

import os

def validate_file_extension(value):    
    
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.geojson']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

# Create your models here.
class ImagesLocation(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    img = models.FileField(upload_to="",null=True,blank=True,validators=[validate_file_extension])
    poly = models.MultiPolygonField(null=True,blank=True)