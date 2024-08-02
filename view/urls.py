from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.home),
    path('auth/login', views.login),
    path("__reload__/", include("django_browser_reload.urls")),
]