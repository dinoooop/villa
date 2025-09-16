from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Profile
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.models import BaseUserManager
from villa.utils import generate_random_password

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("name") # Full name.
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            # handle duplicate email
            return render(request, "register.html", {"error": "Email already exists"})

        # use email as username
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
        )
        login(request, user)
        return redirect("profile")

    return render(request, "account/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # find the user by email
            user_obj = User.objects.get(email=email)
            username = user_obj.username  # get username (since auth needs username)
        except User.DoesNotExist:
            return render(request, "account/login.html", {"error": "Invalid email or password"})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect admin to /cadmin
            if user.is_superuser:
                return redirect("/cadmin/builders/")
            return redirect("profile")
        else:
            return render(request, "account/login.html", {"error": "Invalid email or password"})

    return render(request, "account/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")


def profile_view(request):
    user = request.user  # logged-in user
    profile = Profile.objects.filter(user=user).first()  # get profile if exists
    return render(request, "account/profile.html", {"user": user, "profile": profile})

def profile_edit(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        about = request.POST.get("about")
        # Update user details
        user.first_name = first_name
        user.email = email
        user.username = email
        user.save()

        if profile:
            # Update existing profile
            profile.phone = phone
            profile.about = about
            profile.save()
        else:
            # Create new profile if it doesn't exist
            profile = Profile.objects.create(user=user, phone=phone, about=about)
            profile.save()  # save the profile

        return redirect("profile")
    return render(request, "account/profile_edit.html", {"user": user, "profile": profile})

def security_edit(request):
    user = request.user
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            return render(request, "security.html", {"error": "Passwords do not match"})
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()

            return redirect("login")
        else:
            return render(request, "security.html", {"error": "Current password is incorrect"})
    
    return render(request, "account/security.html", {"user": user})


@login_required
def avatar_update(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST" and request.FILES.get("avatar"):
        profile.avatar = request.FILES["avatar"]
        profile.save()
        return JsonResponse({"success": True, "avatar_url": profile.avatar.url})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# Read
def list_users(request):
    # populate profile details
    users = User.objects.select_related('profile').exclude(is_superuser=True)
    return render(request, 'account/list_users.html', {'users': users})

def create_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name") # Full name.
        email = request.POST.get("email")
        # give random password
        password = generate_random_password()
        phone = request.POST.get("phone")
        about = request.POST.get("about")

        if User.objects.filter(email=email).exists():
            # handle duplicate email
            return render(request, "register.html", {"error": "Email already exists"})

        # use email as username
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
        )

        # create profile
        profile = Profile.objects.create(user=user, phone=phone, about=about)

        # Handle cropped avatar
        cropped_avatar_data = request.POST.get("cropped_image_data")
        if cropped_avatar_data:
            format, imgstr = cropped_avatar_data.split(';base64,')
            ext = format.split('/')[-1]
            profile.avatar.save(f"avatar_{user.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=True)

        return redirect('list_users')
    return render(request, 'account/create_user.html')

# Update
def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    profile = user.profile
    if request.method == "POST":
        user.first_name = request.POST['first_name']
        user.email = request.POST['email']
        user.username = request.POST['email']
        profile.phone = request.POST['phone']
        profile.about = request.POST.get("about")

        # Handle cropped avatar
        cropped_avatar_data = request.POST.get("cropped_image_data")
        if cropped_avatar_data:
            format, imgstr = cropped_avatar_data.split(';base64,')
            ext = format.split('/')[-1]
            profile.avatar.save(f"avatar_{user.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=True)
        
        user.save()
        profile.save()
        return redirect('list_users')
    
    return render(request, 'account/edit_users.html', {'user': user, 'profile': profile})

# Delete
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('list_users')
