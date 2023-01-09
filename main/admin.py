from django.contrib import admin
from .models import Raster,Vector,Dataset,Profile,RasterData,VectorData
# Register your models here.

admin.site.site_header = "WebGIS Admin"
admin.site.site_title = "WebGIS"
admin.site.index_title = "You're on the administration of the WebGIS"


admin.site.register(Raster)
admin.site.register(Vector)
admin.site.register(Dataset)
admin.site.register(Profile)
admin.site.register(VectorData)