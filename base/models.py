from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import User



# Create your models here.
class ShortenUrl(models.Model):
    author = models.ForeignKey(User, related_name='url', on_delete=models.CASCADE, null=True)
    longurl = models.URLField()
    shorturl = models.URLField()
    tags = models.CharField(max_length=500, null=True, default=None)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateField(auto_now=True)
    
    
    
class Profile(models.Model):
    author = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE, null=False)
    profile_pics = models.URLField(default='image/Solo-Leveling-Sung-jin-woo.jpg')
    bio = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)