from django import forms
from .models import ImageUpload

class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget = forms.FileInput(attrs={'class': 'form-control','id': 'inputGroupFile02' }),label='')
    class Meta:
        model = ImageUpload
        fields = ['image']
