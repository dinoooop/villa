from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Project
from django.contrib.auth.models import User
import base64
from django.core.files.base import ContentFile
from villa.utils import utils_create_project

# Create a new project
def create_project(request):
    if request.method == "POST":
        project = utils_create_project(request=request)
        return redirect('list_project')
    users = User.objects.exclude(is_superuser=True)
    return render(request, "project/create_project.html", {"users": users})

def front_create_project(request):
    if request.method == 'POST':
        project = utils_create_project(request=request)
        return redirect('front_list_project')
    users = User.objects.exclude(is_superuser=True)
    return render(request, "project/front_create_project.html", {"users": users})

# Edit an existing project
def edit_project(request, id):
    
    project = get_object_or_404(Project, id=id)
    users = User.objects.exclude(is_superuser=True)

    if request.method == "POST":
        project.title = request.POST.get("title")
        project.description = request.POST.get("description")
        project.price = request.POST.get("price")
        project.bedrooms = request.POST.get("bedrooms")
        project.bathrooms = request.POST.get("bathrooms")
        project.area = request.POST.get("area")
        project.floor = request.POST.get("floor")
        project.parking = request.POST.get("parking")
        project.save()

        cropped_image_data = request.POST.get("cropped_image_data")
        if cropped_image_data:
            format, imgstr = cropped_image_data.split(';base64,')
            ext = format.split('/')[-1]
            project.image.save(f"project_{project.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=True)

        return redirect("list_project")

    return render(request, "project/edit_project.html", {"project": project, "users": users})

# Delete a project
def delete_project(request, id):
    project = get_object_or_404(Project, id=id)
    project.delete()
    return redirect("list_project")

def list_project(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, "project/list_project.html", {"projects": projects})

def front_list_project(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, "project/front_list_project.html", {"projects": projects})




