from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import ShortenUrl, Profile

class ShortenUrlAdmin(ModelAdmin):
    list_display=("author", "shorturl", "longurl")

class ProfileAdmin(ModelAdmin):
    list_display=("author", "bio")

# Register your models here.
admin.site.register(ShortenUrl, ShortenUrlAdmin)
admin.site.register(Profile, ProfileAdmin)