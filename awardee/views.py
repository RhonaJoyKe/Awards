from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse,Http404
from .models import Project,Profile,Rating

# Create your views here.
def home(request):
    return render(request,'index.html')

