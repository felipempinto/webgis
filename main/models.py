from django.db import models
from django.contrib.gis.db import models as modelsgis
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
from django.forms import ValidationError
from django.template.defaultfilters import filesizeformat
from django.contrib.humanize.templatetags import humanize

from functools import partial
import os

#############################################
# FUNCTIONS
def validate_file_extension_vector(value):    
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.geojson']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def validate_file_extension_raster(value):    
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.tif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def upload_to(instance, filename,path):
    return f'dataset/{instance.user.username}/{path}/{filename}' 

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
    image = models.ImageField(default='default.jpg', upload_to=upload_to_path('profile'),null=True,blank=True)
    bio = models.TextField(default='',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Dataset(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User,related_name = 'owner_dataset',on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_path('dataset'),null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_created_at(self):
        return humanize.naturaltime(self.created_at)

class Vector(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User,related_name = 'owner_vector',on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_path('vector'),validators=[validate_file_extension_vector])
    # downloaded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_created_at(self):
        return humanize.naturaltime(self.created_at)

class Raster(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User,related_name = 'owner_raster',on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_path('raster'),validators=[validate_file_extension_raster])
    # downloaded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_created_at(self):
        return humanize.naturaltime(self.created_at)

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

    
    