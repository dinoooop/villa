from django.urls import path
from . import views

urlpatterns = [
    # accounts
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/avatar/", views.avatar_update, name="avatar_update"),
    path("security/", views.security_edit, name="security_edit"),
    
]
