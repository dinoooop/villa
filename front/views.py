from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from project.models import Project
# Create your views here.
def home(request):
    return render(request, 'general/home.html')

def properties(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, 'general/properties.html', {'projects': projects})

def contact(request):
    return render(request, 'general/contact.html')