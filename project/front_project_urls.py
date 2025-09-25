# accounts/cadmin_urls.py
from django.urls import path
from . import front_project_views

urlpatterns = [
    path('', front_project_views.list_project, name='front_list_project'),
    path('create/', front_project_views.create_project, name='front_create_project'),
    path('edit/<int:pk>/', front_project_views.edit_project, name='front_edit_project'),
    path('delete/<int:pk>/', front_project_views.delete_project, name='front_delete_project'),
    path('details/<int:pk>/', front_project_views.detail_project, name='front_detail_project'),
]
