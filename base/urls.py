from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('url', views.convert_url, name='convert.url'),
    path('auth/login', views.userLogin, name="auth.login"),
    path('auth/register', views.userregistration, name="auth.register"),
]