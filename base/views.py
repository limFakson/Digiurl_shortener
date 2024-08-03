import re
from django.shortcuts import render
from decouple import config

from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth.models import User
from .models import ShortenUrl
from .serializer import UrlSerializer, UserSerializer
from .functions import hashing


config_file_path = "../.env"

@api_view(['POST', 'GET'])
def convert_url(request):
    if request.method == 'POST':
        try:
            user = request.user
            longurl = request.data.get('url')

            if not longurl:
                return Response({"message": "Need to pass URL"}, status=400)

            if user.is_authenticated:
                author = User.objects.filter(username=user).first()
            else:
                author = None
                
            existing_url = ShortenUrl.objects.filter(longurl=longurl).first()

            if existing_url:
                serializer = UrlSerializer(existing_url)
                return Response(serializer.data, status=200)

            # If URL is not found, create a new shortened URL
            cleaned_url = longurl.replace('?', '').replace('=', '').replace('_', '').replace('-', '')
            url_parts = cleaned_url.split('/')
            url_key = url_parts[-1] + author.username if url_parts and user.is_authenticated else url_parts[-1]
            short = hashing(url_key)
            short_url = config("WEBSITE_URL") + '/' + short

            data = {
                "longurl": longurl,
                "shorturl": short_url,
                "author": author.id if author else None
            }
            serializer = UrlSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        except Exception as e:
            return Response({"message": str(e)}, status=500)
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
        username = user.username
        return Response(
        {"message": "Login successful", "token": token.key, "user_id": user.id},
        status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
        
        
