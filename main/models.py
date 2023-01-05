from django.db import models
from django.contrib.gis.db import models as modelsgis
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

import os

def validate_file_extension(value):    
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.geojson']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def upload_to(instance, filename):
    return 'vector/%s/%s' % (instance.user.user.username, filename)

# Create your models here.
class Vector(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='vectors')
    file = models.FileField(upload_to=upload_to,null=True,blank=True,validators=[validate_file_extension])
    created_at = models.DateTimeField(auto_now_add=True)

class Raster(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='rasters')
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class VectorData(models.Model):
    file = models.OneToOneField(Vector,on_delete=models.CASCADE)
    geom = modelsgis.GeometryField()
    properties = models.CharField(max_length=1000)
    



