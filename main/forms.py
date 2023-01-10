from django import forms
from .models import Vector,Raster,Dataset


class RasterUploadForm(forms.ModelForm):
    class Meta:
        model = Raster
        fields = ["name","file"]
        help_texts = {
            'name': None,
            'file': None,
        }

    def __init__(self, *args, **kwargs): 
        super(RasterUploadForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['file'].label = ''


class VectorUploadForm(forms.ModelForm):

    class Meta:
        model = Vector
        fields = ["name","file"]
        help_texts = {
            'name': None,
            'file': None,
        }

    def __init__(self, *args, **kwargs): 
        super(VectorUploadForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['file'].label = ''

class DatasetUploadForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = ["name","file"]
        help_texts = {
            'name': None,
            'file': None,
        }

    def __init__(self, *args, **kwargs): 
        super(DatasetUploadForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['file'].label = ''
