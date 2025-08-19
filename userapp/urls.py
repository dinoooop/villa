from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_users, name='list_users'),
    path('add/', views.add_user, name='add_user'),
    path('edit/<int:id>/', views.edit_user, name='edit_user'),
    path('delete/<int:id>/', views.delete_user, name='delete_user'),
]
