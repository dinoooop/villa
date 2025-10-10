
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Visit
import razorpay


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_visit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        price = 200
        scheduled_date_time = request.POST.get("scheduled_date_time")
        amount = price * 100  # amount in paise

        visit = project.visits.create(
            name=name,
            email=email,
            phone=phone,
            scheduled_date_time=scheduled_date_time,
        )

        # create Razorpay order
        order = razorpay_client.order.create(dict(
            amount=amount,
            currency="INR",
            payment_capture="1"
        ))

        # create checkout
        checkout = visit.checkouts.create(
            order_id=order["id"],
            amount=price,
            status="pending"
        )

        return redirect("checkout", order_id=checkout.order_id)

    return render(request, "project/front_detail_project.html", {"project": project})

def list_visit(request):
    visits = Visit.objects.filter(project__builder=request.user).order_by("-scheduled_date_time")
    return render(request, "project/front_list_visit.html", {"visits": visits})
