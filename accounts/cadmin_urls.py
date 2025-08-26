# accounts/cadmin_urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_users, name='list_users'),
    path('create/', views.create_user, name='create_user'),
    path('edit/<int:id>/', views.edit_user, name='edit_user'),
    path('delete/<int:id>/', views.delete_user, name='delete_user'),
]
