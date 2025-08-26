# accounts/cadmin_urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.front_create_project, name='front_create_project'),
]
