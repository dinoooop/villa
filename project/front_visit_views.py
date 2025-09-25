from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Visit

def create_visit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

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
        return redirect("front_detail_project", pk=project.id)

    return render(request, "project/front_detail_project.html", {"project": project})

def list_visit(request):
    visits = Visit.objects.filter(project__builder=request.user).order_by("-scheduled_date_time")
    return render(request, "project/front_list_visit.html", {"visits": visits})
