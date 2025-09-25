from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Project
from villa.utils import save_cropped_image, get_statuses
from .forms import ProjectForm

# List all projects
def list_project(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, "project/admin_list_project.html", {"projects": projects})

# Create a new project
def create_project(request):    
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.builder = User.objects.get(id=request.POST["builder"]) if request.POST.get("builder") else request.user
            project.save()
            save_cropped_image(request, project)
            return redirect("admin_list_project")
    else:
        form = ProjectForm()
    return render(
        request,
        "project/admin_create_project.html",
        {
            "form": form, 
            "builders": User.objects.exclude(is_superuser=True), 
            "statuses": get_statuses(), 
        },
    )

# Edit an existing project
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.builder = User.objects.get(id=request.POST["builder"]) if request.POST.get("builder") else request.user
            project.save()
            save_cropped_image(request, project)
            return redirect("admin_list_project")
    else:
        form = ProjectForm(instance=project)
    return render(
        request,
        "project/admin_edit_project.html",
        {
            "form": form, 
            "builders": User.objects.exclude(is_superuser=True), 
            "statuses": get_statuses(), 
            "project": project
        },
    )

# Delete a project
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect("admin_list_project")

