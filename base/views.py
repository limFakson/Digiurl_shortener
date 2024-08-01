from django.shortcuts import render
from decouple import config


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import ShortenUrl
from .serializer import UrlSerializer
from .hashing import hashing


config_file_path = "../.env"

@api_view(['POST', 'GET'])
def convert_url(request):
    if request.method == 'POST':
        longurl = request.data.get('url')
        existing_url = ShortenUrl.objects.filter(longurl=longurl)
        if not existing_url.exists():
            url = list(longurl.split('/'))
            url = url[-1]
            short = hashing(str(url))
            short = config("WEBSITE_URL") + '/' + short
            
            serializer = UrlSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(longurl= longurl,shorturl=short)
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            existing_url = ShortenUrl.objects.get(longurl=longurl)
            longurl = existing_url.longurl
            shorturl = existing_url.shorturl
            author = existing_url.author
            data = {
                "author":author,
                "shorturl":shorturl,
                "longurl":longurl
            }
            print(longurl, shorturl)
            return Response(data, 200)

