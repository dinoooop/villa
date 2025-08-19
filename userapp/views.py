from django.shortcuts import render, redirect, get_object_or_404
from .models import User

# Create
def add_user(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        User.objects.create(name=name, email=email, phone=phone)
        return redirect('list_users')
    return render(request, 'cadmin/userapp/add_user.html')

# Read
def list_users(request):
    users = User.objects.all()
    return render(request, 'cadmin/userapp/list_users.html', {'users': users})

# Update
def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.save()
        return redirect('list_users')
    return render(request, 'cadmin/userapp/edit_users.html', {'user': user})

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

        