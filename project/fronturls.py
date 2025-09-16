# accounts/cadmin_urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.front_list_project, name='front_list_project'),
    path('create/', views.front_create_project, name='front_create_project'),
]
