from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib import messages 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404

from .models import RasterData,VectorData,Raster,Vector,Dataset
from .forms import DatasetUploadForm,VectorUploadForm,RasterUploadForm
import json,os

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


def user(request):
    return render(
        request,
        template_name='main/user_page.html'
    )

@login_required(login_url='/login/')
def download_page(request):
    user = request.user

    raster_datasets = Raster.objects.filter(user=user)
    vector_datasets = Vector.objects.filter(user=user)
    other_datasets = Dataset.objects.filter(user=user)

    raster_form = RasterUploadForm(instance=request.user)
    vector_form = VectorUploadForm(instance=request.user)
    dataset_form = DatasetUploadForm(instance=request.user)

    data = {
        "raster": raster_datasets, 
        "vector": vector_datasets,
        'other':other_datasets
    }

    return render(
            request, 
            "main/download_page.html", 
            {'data':data,
            'rf':raster_form,
            'vf':vector_form,
            'df':dataset_form
            }
            )

@login_required(login_url='/login/')
def map(request):
    vector = Vector.objects.filter(user=request.user)

    dataset = {}
    for f in vector:
        vector_data2 = VectorData.objects.filter(user=request.user).filter(file=f)
        dataset[f.file] = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": json.loads(data.properties),
            "geometry": json.loads(data.geom.geojson)
        }
        for data in vector_data2
    ]
    }
    

    vector_data = VectorData.objects.filter(user=request.user)
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

    return render(
        request,
        template_name='main/map.html',
        context={
            'geojson':json.dumps(geojson),
            'dataset':dataset,
        }
    )

@login_required(login_url='/login/')
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

            vector_data = VectorData.objects.create(
                file=vector,
                user=vector.user,
                geom=GEOSGeometry(feat.geom.wkt),
                properties=data,
            )
            vector_data.save()

            vector.created=True
            vector.save(update_fields=['created'])

        messages.success(request, 'Vector data created successfully!')
    
    raster_id = request.GET.get('raster_id')
    if raster_id is not None:
        raster = Raster.objects.get(pk=raster_id)

        if raster.user != request.user:
            messages.error(request,"Error while trying to create view")
            return redirect('main:homepage')

        # messages.success(request, 'raster data created successfully!')
        messages.info(request,"Resource not ready yet!")

    # Redirect to the same page
    return redirect(request.META.get('HTTP_REFERER'))


def delete(model,request):
    if model.user==request.user:
        model.delete()
        return True
    else:
        return False

@login_required(login_url='/login/')
def deleteview(request,source,dataid):

    if source=='raster':
        model = get_object_or_404(RasterData, pk=dataid)
    elif source=='vector':
        model = get_object_or_404(VectorData, pk=dataid)

    delete(model,request)
    return redirect("main:download")

def deletedata(request,source,dataid):
    if source=='raster':
        model = get_object_or_404(Raster, pk=dataid)
    elif source=='vector':
        model = get_object_or_404(Vector, pk=dataid)
    elif source=='other':
        model = get_object_or_404(Dataset, pk=dataid)


    delete(model,request)
    return redirect("main:download")

@login_required(login_url='/login/')
def uploaddata(request,source):

    if request.method == 'POST':
        file_name = request.POST.get(f'name-{source}')
        uploaded_file = request.FILES[f'file-{source}']
        
        if source == 'raster':
            raster = Raster(name=file_name, file=uploaded_file,user=request.user)
            raster.save()
        elif source == 'vector':
            vector = Vector(name=file_name, file=uploaded_file,user=request.user)
            vector.save()
        else:
            dataset = Dataset(name=file_name, file=uploaded_file,user=request.user)
            dataset.save()

    return redirect('main:download')