# accounts/cadmin_urls.py
from django.urls import path
from . import front_visit_views

urlpatterns = [
    path('', front_visit_views.list_visit, name='front_list_visit'),
    path('create/<int:project_id>/', front_visit_views.create_visit, name='front_create_visit'),
    


]
