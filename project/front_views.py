from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Project
from django.contrib.auth.models import User
import base64
from django.core.files.base import ContentFile
from .models import Visit
# Create a new project
def create_project(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        bedrooms = request.POST.get("bedrooms")
        bathrooms = request.POST.get("bathrooms")
        area = request.POST.get("area")
        floor = request.POST.get("floor")
        parking = request.POST.get("parking")
        builder = request.user.id

        project = Project.objects.create(
            title=title,
            description=description,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area=area,
            floor=floor,
            parking=parking,
            price=price,
            builder=User.objects.get(id=builder),
        )

        cropped_image_data = request.POST.get("cropped_image_data")
        if cropped_image_data:
            format, imgstr = cropped_image_data.split(';base64,')
            ext = format.split('/')[-1]
            project.image.save(f"project_{project.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=True)
        return redirect("profile")  # Redirect to list after creation

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

        return redirect("front_list_project")

    return render(request, "project/front_edit_project.html", {"project": project, "users": users})


# Delete a project
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.delete()
        return redirect("list_project")

    return render(request, "project/delete_project.html", {"project": project})


# List all projects
def list_project(request):
    projects = Project.objects.filter(builder=request.user).order_by("-created_at")
    return render(request, "project/front_list_project.html", {"projects": projects})

def list_visits(request):
    visits = Visit.objects.filter(project__builder=request.user).order_by("-scheduled_date_time")
    return render(request, "project/front_list_visits.html", {"visits": visits})


def front_detail_project(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, "project/front_detail_project.html", {"project": project})


def schedule_visit_project(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        scheduled_date_time = request.POST.get("scheduled_date_time")
        project.visits.create(
            name=name,
            email=email,
            phone=phone,
            scheduled_date_time=scheduled_date_time,
        )
        return redirect("front_detail_project", id=project.id)

    return render(request, "project/front_detail_project.html", {"project": project})