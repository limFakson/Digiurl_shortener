from django.shortcuts import redirect
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.db import connections
from django.utils.deprecation import MiddlewareMixin

from .functions import RedirectToUrl
from decouple import config

config_file_path = "../.env"

class RedirectUrl(MiddlewareMixin):
    def process_request(self, request):
        try:    
            domain = request.get_full_path()
            sort_url = domain.split('/')
            if len(sort_url) > 1 and sort_url[1] not in ["page", "admin"]:
                base_url = config("WEBSITE_URL")
                url = base_url + "/" + sort_url[1]
                link = RedirectToUrl(url)
                print(link)
                return HttpResponseRedirect(link)
        except Exception as e:
            print(f"An error occurred: {e}")
            
        return None