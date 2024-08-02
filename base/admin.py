from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import ShortenUrl

class ShortenUrlAdmin(ModelAdmin):
    list_display=("author", "shorturl", "longurl")

# Register your models here.
admin.site.register(ShortenUrl, ShortenUrlAdmin)