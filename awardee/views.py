from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse,Http404
from .models import AddProjectForm, Project,Profile,Rating
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'index.html')
def add_image(request):
    if request.method=='POST':
        current_user=request.user
        form=AddProjectForm(request.POST,request.FILES)
        if form.is_valid():
            image=form.save(commit=False)
            image.user=current_user
            image.save()
            messages.success(request,('Image was posted successfully!'))
            return redirect('home')
    else:
            form=AddProjectForm()
    return render(request,'add_project.html',{'form':form})

