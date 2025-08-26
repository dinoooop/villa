# accounts/cadmin_urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_project, name='list_project'),
    path('create/', views.create_project, name='create_project'),
    path('edit/<int:id>/', views.edit_project, name='edit_project'),
    path('delete/<int:id>/', views.delete_project, name='delete_project'),
]
