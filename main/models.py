from django.db import models
from django.contrib.gis.db import models as modelsgis
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
from django.forms import ValidationError
from django.template.defaultfilters import filesizeformat

from functools import partial
import os

#############################################
# FUNCTIONS
def validate_file_extension(value):    
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.geojson']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def upload_to(instance, filename,path):
    return f'dataset/{instance.user.user.username}/{path}/{filename}' 

def upload_to_path(path):
    return partial(upload_to, path=path)

def clean_content(self):
    content = self.cleaned_data['content']
    if content._size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(f'Please keep filesize under {filesizeformat(settings.MAX_UPLOAD_SIZE)}. Current filesize {filesizeformat(content._size)}')
    return content

#############################################
## MODELS
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to='static/images')
    bio = models.TextField(default='',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Dataset(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=upload_to_path('dataset'),null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Vector(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='vectors')
    file = models.FileField(upload_to=upload_to_path('vector'),null=True,blank=True,validators=[validate_file_extension])
    downloaded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Raster(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='rasters')
    file = models.FileField(upload_to=upload_to_path('vector'),null=True,blank=True,validators=[validate_file_extension])
    downloaded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class VectorData(models.Model):
    file = models.OneToOneField(Vector,on_delete=models.CASCADE)
    geom = modelsgis.GeometryField()
    properties = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RasterData(models.Model):
    file = models.OneToOneField(Raster,on_delete=models.CASCADE)
    path = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    



