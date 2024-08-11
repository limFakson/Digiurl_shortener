import os
import re
from pathlib import Path
from decouple import config
from django.conf import settings
from django.shortcuts import render


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status


from .functions import hashing
from .models import ShortenUrl, Profile
from django.contrib.auth.models import User
from .serializer import UrlSerializer, UserSerializer, ProfileSerializer



config_file_path = "../.env"



@api_view(['POST', 'GET'])
def convert_url(request):
    if request.method == 'POST':
        try:
            user = request.user  
        except:
            return Response({"message": "not working"}, status=500)
        
        
        longurl = request.data.get('url')


        if not longurl:
            return Response({"message": "Need to pass URL"}, status=400)

           
            
        existing_url = ShortenUrl.objects.filter(longurl=longurl).first()
        
        
        if existing_url:
            serializer = UrlSerializer(existing_url)
            return Response(serializer.data, status=200)


        # If URL is not found, create a new shortened URL
        cleaned_url = longurl.replace('?', '').replace('=', '').replace('_', '').replace('-', '')
        url_parts = cleaned_url.split('/')
        url_key = url_parts[-1] + user.username if url_parts and user.is_authenticated else url_parts[-1]
        short = hashing(url_key)
        short_url = config("WEBSITE_URL") + '/' + short
        data = {
            "longurl": longurl,
            "shorturl": short_url,
            "author": user.id if user.is_authenticated else None
        }
        
        serializer = UrlSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    
    return Response()  




# Registration Authetication view
@csrf_protect
@api_view(["POST"])
def userregistration(request):
    """
    Handling Auth of the Users

    """


    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            
            #filter for existing user
            if User.objects.filter(username=username).exists():
                return Response({"message":"Username already taken"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            elif User.objects.filter(email=email).exists():
                return Response({"message":"Email associated with another account"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            else:
                try:
                    new_user = User.objects.create_user(
                        username=username, email=email, password=password
                    )
                    serializer_user = UserSerializer(new_user)
                    user = authenticate(request, username=username, password=password)
                    token, created = Token.objects.get_or_create(user=user)
                    login(request, user)
                    return Response({"message":"User sucessfully created", "token":token.key}, status=200)
                
                except:
                    return Response({"message":"User already exist"}, status=status.HTTP_400_BAD_REQUEST)
            
        
        else:
            return Response(serializer.errors, status=400)
       
       
        
# Login Authentication View
@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def userLogin(request):
    credential = request.data.get("credential")
    password = request.data.get("password")


    if not credential or not password:
        return Response(
            {"message": "Invalid request. Both credential and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    
    is_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    
    
    if re.match(is_email, credential):
        name = User.objects.filter(email=credential)
        user = authenticate(request, username=name[0], password=password)
   
    else:
        user = authenticate(request, username=credential, password=password)

    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response(
        {"message": "Login successful", "token": token.key, "user_id": user.id},
        status=status.HTTP_200_OK)
   
    else:
        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
        

@api_view(['POST', 'GET'])
def profile(request):
    try:
        user = request.user  
    except:
        return Response({"message": "not working"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    if request.method == "POST":
        
        profile_pics = request.FILES.get('profile_pics')
        bio = request.data.get("bio")
        
        if user.is_authenticated: 
            author = user
        else: 
            return Response({"message":"You need to login to edit profile"}, status=401)
        
        
        if profile_pics:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(profile_pics.name, profile_pics)
            image_url = fs.url(filename)
            
            
            data = {
                "author":author.id,
                'bio':bio,
                'profile_pics': image_url
            }
            
            
            serializer = ProfileSerializer(data=data)
            
            
            if serializer.is_valid():
                # Check if the user already has a profile and delete the existing profile picture
                try:
                    profile = Profile.objects.get(author=user)
                    if profile.profile_pics:
                        old_image_path = os.path.join(BASE_DIR, f'view/theme{profile.profile_pics}')
                        
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                        profile.delete()
                        
                except Profile.DoesNotExist:
                    pass
                
                serializer.save(profile_pics=f'/static{image_url}')
                return Response({"message": "Uploaded successfully"}, status=status.HTTP_201_CREATED)
            
            
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": "Profile picture is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    elif request.method == "GET":
        if not user.is_authenticated:
            return Response({"message":"You need to login to view profile"}, status=status.HTTP_401_UNAUTHORIZED)
        
        profile = Profile.objects.filter(author=user).first()
        if profile:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    return Response({"message": "Request not accepted"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)