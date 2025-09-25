from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from project.models import Project
# Create your views here.
def home(request):
    return render(request, 'general/home.html')

def properties(request):
    projects = Project.objects.filter(status='approved').order_by("-created_at")
    other = {
        'page': 'properties',
        'heading': 'Properties',
        'sub_heading': 'We Provide The Best Property You Like',
    }
    return render(request, "project/front_list_project.html", {"projects": projects, "other": other})

def contact(request):
    return render(request, 'general/contact.html')