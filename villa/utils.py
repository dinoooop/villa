import secrets
import string
from project.models import Project
from django.contrib.auth.models import User
import base64
from django.core.files.base import ContentFile


def generate_random_password(length=12):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def utils_create_project(request):
    title = request.POST.get("title")
    description = request.POST.get("description")
    price = request.POST.get("price")
    bedrooms = request.POST.get("bedrooms")
    bathrooms = request.POST.get("bathrooms")
    area = request.POST.get("area")
    floor = request.POST.get("floor")
    parking = request.POST.get("parking")
    status = 'pending'
    builder = request.POST.get("builder")

    project = Project.objects.create(
        title=title,
        description=description,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        area=area,
        floor=floor,
        parking=parking,
        status=status,
        price=price,
        builder=User.objects.get(id=builder),
    )

    cropped_image_data = request.POST.get("cropped_image_data")
    
    if cropped_image_data:
        format, imgstr = cropped_image_data.split(';base64,')
        ext = format.split('/')[-1]
        project.image.save(f"project_{project.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=True)
        
    return project


def save_cropped_image(request, model_instance):
    cropped_image_data = request.POST.get("cropped_image_data")
    if cropped_image_data:
        format, imgstr = cropped_image_data.split(';base64,')
        ext = format.split('/')[-1]
        model_instance.image.save(f"cropped_{model_instance.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=True)
    

def get_statuses():
    return {
        'pending': 'Pending',
        'approved': 'Approved',
        'sold': 'Sold'
    }



