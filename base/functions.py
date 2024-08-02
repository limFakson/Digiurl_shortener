import base62
import hashlib
import random

from django.shortcuts import redirect
from .models import ShortenUrl

def hashing(keyword):
    # Hash the keyword using SHA-256 to get a fixed-length output
    hash_object = hashlib.sha256(keyword.encode('utf-8'))
    hex_dig = hash_object.hexdigest()

    # Convert the hex digest to an integer
    num = int(hex_dig, 16)

    # Encode the integer to base62
    base62_encoded = base62.encode(num)

    # Ensure the result is exactly 5 characters long
    # If the encoded string is shorter than 5 characters, pad it
    # If it is longer, truncate it
    short = base62_encoded[:5].rjust(5, '0')
    
    return short

def RedirectToUrl(url):
    longurl = ShortenUrl.objects.get(shorturl=url)
    new_link = longurl.longurl
    return new_link