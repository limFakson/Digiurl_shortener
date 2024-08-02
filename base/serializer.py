from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ShortenUrl

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=400)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        
class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenUrl
        fields = [
            'author',
            'longurl',
            'shorturl'
        ]
        read_only_fields = ["longurl", "shorturl", "author"]