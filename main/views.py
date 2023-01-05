from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib import messages 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import VectorData,Raster,Vector
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


from django.shortcuts import render

def download_page(request):
    # Get the current user
    user = request.user

    # Get the user's raster datasets
    raster_datasets = Raster.objects.filter(user=user)

    # Get the user's vector datasets
    vector_datasets = Vector.objects.filter(user=user)

    # Render the download page template with the raster and vector datasets
    return render(request, "download_page.html", {"raster_datasets": raster_datasets, "vector_datasets": vector_datasets})


