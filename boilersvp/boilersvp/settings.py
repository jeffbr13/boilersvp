"""
Django settings for boilersvp project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import logging
import os
import sys

import environ

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'huey.contrib.djhuey',
)

LOCAL_APPS = (
    'subscriptions',
)


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'boilersvp.urls'

SITE_NAME = 'boilersvp'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'boilersvp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

# Huey task queue
# http://huey.readthedocs.io/en/latest/django.html
HUEY = {
    'always_eager': False,
    'connection': {
        'url': str(env.cache_url('REDIS_URL')),
    },
}

# LOGGING CONFIGURATION
default_app_logger = {
    'handlers': ['console'],
    'level': logging.DEBUG if DEBUG else logging.INFO,
    'propagate': False
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        # default log handler prints to console at debug level
        'console': {
            'level': logging.DEBUG if DEBUG else logging.INFO,
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple',
        },
    },
    'loggers': {app: default_app_logger for app in LOCAL_APPS},
}

# Email
# https://docs.djangoproject.com/en/1.11/topics/email#django.core.mail.backends.smtp.EmailBackend
SERVER_EMAIL = env.str('SERVER_EMAIL', 'boilersvp@benjeffrey.net')
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env.str('MAILGUN_SMTP_SERVER')
    EMAIL_PORT = env.str('MAILGUN_SMTP_PORT')
    EMAIL_HOST_USER = env.str('MAILGUN_SMTP_LOGIN')
    EMAIL_HOST_PASSWORD = env.str('MAILGUN_SMTP_PASSWORD')
    EMAIL_USE_TLS = True

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

root = environ.Path(__file__) - 3  # three folder back (/a/b/c/ - 3 = /)
SITE_ROOT = root()
public_root = root.path('public/')
MEDIA_ROOT = public_root('media')
MEDIA_URL = '/media/'
STATIC_ROOT = public_root('static')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
