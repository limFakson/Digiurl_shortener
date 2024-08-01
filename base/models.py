from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShortenUrl(models.Model):
    author = models.ForeignKey(User, related_name='url', on_delete=models.CASCADE, null=True)
    longurl = models.URLField()
    shorturl = models.URLField()