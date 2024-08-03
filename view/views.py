from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout

from base.serializer import UserSerializer
from base.models import ShortenUrl

# Create your views here.
def home(request):
    try:
        user = request.user
    except:
        user =None
        
    if user.is_authenticated:
        user = User.objects.get(username=user)
        return render(request, 'Page/home.html', {user:user})
    return render(request, 'Page/home.html')


def login(request):
    try:
        user = request.user
    except:
        user =None
        
    if user.is_authenticated:
        return redirect('/short/view/home')
    if request.method == "GET":
        return render(request, 'Auth/login.html')
    
    
def register(request):
    try:
        user = request.user
    except:
        user =None
        
    if user.is_authenticated:
        return redirect('/short/view/home')
    if request.method == "GET":
        return render(request, 'Auth/register.html')


def logout_view(request):
    logout(request)
    return redirect('/short/view/home')


def profile(request):
    try:
        user = request.user
    except:
        user =None
        
    if user.is_authenticated:
        user = User.objects.get(username=user)
        links = ShortenUrl.objects.get(user=user)
        
        return render(request, 'Page/profile.html', {user:user, links:links})
    else:
        return redirect('/short/view/auth/login')
        
