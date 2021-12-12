from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse,Http404
from .models import AddProjectForm, Project,Profile,Rating, UpdateProfileForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    project=Project.objects.all()
    if request.method=='POST':
        current_user=request.user
        form=AddProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.user=current_user
            project.save()
            messages.success(request,('Project was posted successfully!'))
            return redirect('home')
    else:
            form=AddProjectForm()
    return render(request,'index.html',{'form':form,'projects':project})
def profile(request,user_id):
    current_user=get_object_or_404(User,id=user_id)
    # current_user = request.user
    projects = Project.objects.filter(user=current_user)
    profile = get_object_or_404(Profile,id = current_user.id)
    return render(request, 'profile/profile.html', {"projects": projects, "profile": profile})
def update_profile(request):
  	#Get the profile
    current_user=request.user
    profile = Profile.objects.filter(id=current_user.id).first()
    if request.method == 'POST':
        profileform = UpdateProfileForm(request.POST,request.FILES,instance=profile)
        if  profileform.is_valid:
            profileform.save(commit=False)
            profileform.user=request.user
            profileform.save()
            return redirect('profile')
    else:
        form=UpdateProfileForm()
    return render(request,'profile/update_profile.html',{'form':form})


