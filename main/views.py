from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib import messages 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry

from .models import RasterData,VectorData,Raster,Vector,Dataset
import json

def homepage(request):
    return render(request,
    template_name='main/homepage.html')

def logout_request(request):
    logout(request)
    messages.info(request,"You are logged out")
    return redirect("main:homepage")

def login_request(request):
    if request.user.is_authenticated:
        return redirect("main:user")
    else:
        if request.method == "POST":
            form = AuthenticationForm(request,data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username = username,password = password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are logged as {username}")
                    return redirect("main:homepage")
                else:
                    messages.error(request,"Username or password don't match")
            else:
                messages.error(request,"Username or password don't match")
        form = AuthenticationForm()
        return render(request,
                    "main/login.html",
                    {"form":form})



def get_my_shapes(request):
    vector_data = VectorData.objects.all()

    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": json.loads(data.properties),
                "geometry": json.loads(data.geom.geojson)
            }
            for data in vector_data
        ]
    }

    # Add the GeoJSON to the map
    # L.geoJSON(geojson).addTo(map)

def user(request):
    return render(
        request,
        template_name='main/user_page.html'
    )


def download_page(request):
    user = request.user

    raster_datasets = Raster.objects.filter(user=user)
    vector_datasets = Vector.objects.filter(user=user)
    other_datasets = Dataset.objects.filter(user=user)

    data = {
        "raster": raster_datasets, 
        "vector": vector_datasets,
        'other':other_datasets
    }

    return render(
            request, 
            "main/download_page.html", 
            {'data':data}
            )



def map(request):
    return render(
        request,
        template_name='main/map.html'
    )

@login_required
def createdata(request):
    
    vector_id = request.GET.get('vector_id')
    if vector_id is not None:
        vector = Vector.objects.get(pk=vector_id)

        if vector.user != request.user:
            messages.error(request,"Error while trying to create view")
            return redirect('main:homepage')
        
        ds = DataSource(vector.file.url)
        layer = ds[0]
        for feat in layer:
            data = {}
            for i in feat.fields:
                data[i] = feat.get(i)
            data = json.dumps(data)

            print(dir(feat.geom))
            vector_data = VectorData.objects.create(
                file=vector,
                user=vector.user,
                geom=GEOSGeometry(feat.geom.wkt),
                properties=data,
            )
            vector_data.save()

        messages.success(request, 'Vector data created successfully!')
    
    raster_id = request.GET.get('raster_id')
    if raster_id is not None:
        raster = Raster.objects.get(pk=raster_id)

        if raster.user != request.user:
            messages.error(request,"Error while trying to create view")
            return redirect('main:homepage')

        # raster_data = RasterData.objects.create(
        #     file=raster.file,
        #     geom=raster.get_geometry(),
        #     properties=raster.get_properties(),
        # )

        # raster_data.save()

        messages.success(request, 'raster data created successfully!')

    # Redirect to the same page
    return redirect(request.META.get('HTTP_REFERER'))