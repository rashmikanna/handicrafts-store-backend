# project settings.py
from pathlib import Path
import os
import certifi
from mongoengine import connect
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
from corsheaders.defaults import default_headers
from datetime import timedelta

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-default-key-for-dev')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_extensions',
    'rest_framework',
    'rest_framework_simplejwt',
    'nosql_products',
    'nosql_usersdata',
    'nosql_notifications',
    'seller_panel',
    'accounts',
    'producer',
    'captcha',
    'orders',
    'reviews',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'authorization',
]

# URLs
ROOT_URLCONF = 'handicrafts_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'handicrafts_backend.wsgi.application'

# Default database (for auth)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# MongoDB Atlas settings
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'telangana_handicrafts_db')
MONGO_URI = os.getenv('MONGO_URI')

# Connect to MongoDB
connect(
    host=MONGO_URI,
    db=MONGO_DB_NAME,
    alias='default',
    tls=True,
    tlsCAFile=certifi.where(),
)

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'accounts.validators.ComplexPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'handicraft-store-frontend' / 'build' / 'static',
]
STATIC_ROOT = BASE_DIR / 'static'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# Cloudinary configuration (consider moving to env variables too)
cloudinary.config(
    cloud_name='dus8mpxbe',
    api_key='468745917586793',
    api_secret='tgYurWsEfDdYVzeQ3MCjlYhi7so'
)

SIMPLE_JWT = {
    # How long an access token lasts before expiring:
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    # How long a refresh token remains valid:
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    # Automatically issue a new refresh token when you use one:
    'ROTATE_REFRESH_TOKENS': True,
    # After rotation, blacklist the used refresh token:
    'BLACKLIST_AFTER_ROTATION': True,
}

# Email settings for development (use real SMTP in production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", 'srutigoteti@gmail.com')  # Set in .env
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", 'ywfg ojeq jqqn npom')  # Set in .env
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


