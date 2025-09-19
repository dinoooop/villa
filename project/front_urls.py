# accounts/cadmin_urls.py
from django.urls import path
from . import front_views

urlpatterns = [
    path('', front_views.list_project, name='front_list_project'),
    path('visits/', front_views.list_visits, name='front_list_visits'),
    path('create/', front_views.create_project, name='front_create_project'),
    path('edit/<int:id>/', front_views.edit_project, name='front_edit_project'),
    path('schedule-visit/<int:id>/', front_views.schedule_visit_project, name='front_schedule_visit_project'),
    path('delete/<int:id>/', front_views.delete_project, name='front_delete_project'),
    path('details/<int:id>/', front_views.front_detail_project, name='front_detail_project'),
]
