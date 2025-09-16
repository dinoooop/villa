# accounts/cadmin_urls.py
from django.urls import path
from . import front_views

urlpatterns = [
    path('', front_views.list_project, name='front_list_project'),
    path('create/', front_views.create_project, name='front_create_project'),
    path('edit/<int:id>/', front_views.edit_project, name='front_edit_project'),
    path('delete/<int:id>/', front_views.delete_project, name='front_delete_project'),
]
