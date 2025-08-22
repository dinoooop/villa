from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

# Create
def add_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name") # Full name.
        email = request.POST.get("email")
        # give random password
        password = User.objects.make_random_password()
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
            phone=phone,
            about=about
        )

        return redirect('list_users')
    return render(request, 'user/add_user.html')

# Read
def list_users(request):
    # populate profile details
    users = User.objects.select_related('profile').exclude(is_superuser=True)
    return render(request, 'user/list_users.html', {'users': users})

# Update
def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.save()
        return redirect('list_users')
    return render(request, 'user/edit_users.html', {'user': user})

# Delete
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('list_users')


def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        User.objects.create(name=name, email=email, phone=phone)
        # return redirect('profile')
    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
    return render(request, 'login.html')

        