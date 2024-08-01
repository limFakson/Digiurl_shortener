from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ShortenUrl

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenUrl
        fields = [
            'author',
            'longurl',
            'shorturl'
        ]
        read_only_fields = ["longurl", "shorturl", "author"]