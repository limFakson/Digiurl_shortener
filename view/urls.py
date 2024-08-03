from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.home, name="view.home"),
    path('auth/login', views.login, name="view.login"),
    path('auth/register', views.register, name="view.register"),
    path('auth/logout', views.logout_view, name="view.logout"),
    path('profile', views.profile, name="view.profile"),
    path("__reload__/", include("django_browser_reload.urls")),
]