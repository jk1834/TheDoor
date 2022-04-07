from django.urls import path
from .views import dashboard, profile_list, profile, signin, signout, signup, home

app_name = "The Door"

urlpatterns = [
    path("dashboard", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("signup/", signup, name="signup"),
    path("", home, name="home"),
]