# accounts/cadmin_urls.py
from django.urls import path
from . import admin_project_views

urlpatterns = [
    path('', admin_project_views.list_project, name='admin_list_project'),
    path('create/', admin_project_views.create_project, name='admin_create_project'),
    path('edit/<int:pk>/', admin_project_views.edit_project, name='admin_edit_project'),
    path('delete/<int:pk>/', admin_project_views.delete_project, name='admin_delete_project'),
]
