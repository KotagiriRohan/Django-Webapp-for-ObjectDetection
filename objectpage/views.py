from django.shortcuts import render
from .forms import *
# Create your views here.
def home(request):
    context = {'image' : '', 'flag' : False}
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            
            
            return render(request, 'home.html', {'form': form, 'img_obj': img_obj})
    return render(request, 'home.html', {'form': form})