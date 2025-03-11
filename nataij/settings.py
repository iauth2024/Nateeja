"""
Django settings for nataij project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-2au_4jgf7*mxddvcblo(75=b(4ob7tw@i86m2*@!ifs_3k3owi'

DEBUG = False  # Set to False in production, True for local testing

ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ Serve Static Files Properly in Production
if not DEBUG:
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')  # Serves static files efficiently

ROOT_URLCONF = 'nataij.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "results" / "templates"],
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

WSGI_APPLICATION = 'nataij.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static & Media Files Configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'results' / 'static',  # Static files within the app
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Required for `collectstatic`

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Ensure 'media/' directory exists

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
