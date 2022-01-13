from django.shortcuts import render
from .forms import *
from  .objectdetectionmodel import *
# Create your views here.
def home(request):
    context = {'image' : '', 'flag' : False}
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            ObjectDetectionModel('D:/Django/ObjectDetection' + img_obj.image.url)
            mask = '/media/processedimg/Mask.jpg'
            detect = '/media/processedimg/Detect.jpg'
            final = '/media/processedimg/Final.jpg'
            return render(request, 'home.html', {'form': form, 'img_obj': img_obj, 'mask': mask, 'final': final, 'detect': detect})
    return render(request, 'home.html', {'form': form})