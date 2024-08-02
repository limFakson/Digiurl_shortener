import base62
import hashlib
import random

from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import ShortenUrl

def hashing(keyword):
    hash_object = hashlib.sha256(keyword.encode('utf-8'))
    hex_dig = hash_object.hexdigest()

    num = int(hex_dig, 16)
    base62_encoded = base62.encode(num)
    short = base62_encoded[:5].rjust(5, '0')
    
    return short


def RedirectToUrl(url):
    existing_url = ShortenUrl.objects.get(shorturl=url)
    new_link = existing_url.longurl
    return new_link