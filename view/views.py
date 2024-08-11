from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout


from base.serializer import UserSerializer, UrlSerializer
from base.models import ShortenUrl, Profile



# Create your views here.
def revert(request):
    return redirect('/short/view/home')

def home(request):
    try:
        user = request.user
    except:
        user =None
        
        
    if user.is_authenticated:
        try:
            profile = Profile.objects.get(author=user)
        except:
            profile = None
        user = User.objects.get(username=user)
        return render(request, 'Page/home.html', {"user":user, "profile":profile})
    
    return render(request, 'Page/home.html')


def login(request):
    try:
        user = request.user
    except:
        user =None
        
        
    if user.is_authenticated:
        return redirect('/short/view/profile')
    
    if request.method == "GET":
        return render(request, 'Auth/login.html')
    
    
    
def register(request):
    try:
        user = request.user
    except:
        user =None
        
    if user.is_authenticated:
        return redirect('/short/view/profile')
    
    if request.method == "GET":
        return render(request, 'Auth/register.html')




def logout_view(request):
    user = request.user
    token = Token.objects.filter(user=user).delete()
    logout(request)
    return redirect('/short/view/home')


import json
from django.core.serializers.json import DjangoJSONEncoder


def profile(request):
    try:
        user = request.user
    except:
        user =None
    
    if user.is_authenticated:
        user = User.objects.get(username=user)
        try:
            profile = Profile.objects.get(author=user)
        except:
            profile = None
        url = ShortenUrl.objects.filter(author=user.id)
        
        return render(request, 'Page/profile.html', {"user":user, "url":url, "profile":profile})
    else:
        return redirect('/short/view/auth/login')
        
