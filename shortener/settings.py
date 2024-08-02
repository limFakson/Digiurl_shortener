"""
Django settings for shortener project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import dj_database_url
from pathlib import Path
from decouple import config

config_file_path = "../.env"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")
# os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG")
# os.environ.get("DEBUG", "False").lower() == "true"

# allowed host config import
allowed_hosts_str = config("ALLOWED_HOSTS", default="localhost")

# Split the string into a list of allowed hosts
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(",")]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'view.apps.ViewConfig',
    "rest_framework",
    "rest_framework.authtoken",
    'tailwind',
    'view.theme',
    'django_browser_reload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.RedirectUrl',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

INTERNAL_IPS = ALLOWED_HOSTS

ROOT_URLCONF = 'shortener.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'view/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shortener.wsgi.application'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Determine which database to use based on the .env file
if config('DB_CHOICE') == "mysql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('MYSQL_DB_NAME'),
            'USER': config('MYSQL_DB_USER'),
            'PASSWORD': config('MYSQL_DB_PASSWORD', default=''),
            'HOST': config('MYSQL_DB_HOST', default='localhost'),
            'PORT': config('MYSQL_DB_PORT', default='3306'),
            'OPTIONS': {
                'sql_mode': 'STRICT_TRANS_TABLES',
                'charset': 'utf8mb4',
            }
        }
    }
elif config('DB_CHOICE') == "postgres":
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
TAILWIND_APP_NAME = 'view.theme'
print(TAILWIND_APP_NAME)

LOGIN_REDIRECT_URL = '/'

STATIC_URL = 'view.theme/static/'
STATIC_ROOT = BASE_DIR / 'view.theme/static'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_URL = 'static/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
