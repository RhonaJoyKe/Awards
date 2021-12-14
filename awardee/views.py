from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse,Http404
from .models import AddProjectForm, Project,Profile,Rating, UpdateProfileForm,RatingForm
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer


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
    form=AddProjectForm()
    return render(request, 'profile/profile.html', {"projects": projects,'form':form, "profile": profile})
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
def project_details(request, project_id):
  form = RatingForm(request.POST)
  try:
    project_details = Project.objects.get(pk = project_id)
    project_rates = Rating.objects.filter(project__id=project_id).all()
  except Project.DoesNotExist:
    raise Http404
  
  return render(request, 'pro_details.html', {"details":project_details, "rates":project_rates, "form":form})
def search_results(request):
  if 'name' in request.GET and request.GET["name"]:
    name = request.GET.get('name')
    users = Profile.search_profiles(name)
    images = Project.search_project(name)
    print(users)
    return render(request, 'search.html', {"users": users, "project_images": images})
  else:
    return render(request, 'search.html')
def submitrates(request, project_id):
  url = request.META.get('HTTP_REFERER')
  if request.method == 'POST':
    try:
      rating = Rating.objects.get(user__id=request.user.id, project__id=project_id)
      form = RatingForm(request.POST, instance=rating)
      form.save()
      messages.success(request, 'Your rating has been updated')
      return redirect(url)
    except Rating.DoesNotExist:
      form = RatingForm(request.POST)
      if form.is_valid():
        # rating_data = Votes()
        design = form.cleaned_data.get('design')
        userbility = form.cleaned_data.get('userbility')
        content = form.cleaned_data.get('content')
        # form.instance.Avg_score = design_score
        form.instance.project_id=project_id
        form.instance.user_id = request.user.id
        form.save()
        messages.success(request, 'Your rating has been posted')
        
        return redirect(url)
class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)
class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)



