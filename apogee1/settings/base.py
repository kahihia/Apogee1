"""
Django settings for apogee1 project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# points us back to the root folder, where manage.py is
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6fw*ujba!d-3^a8ez_9*da+2@bt2(-1*4@f7bjuvxas$puux_8'

# SECURITY WARNING: don't run with debug turned on in production!
# this just allows the page to send debug messages when somethin goes wrong
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #add django captcha here
    # these are our custom apps
    'parties',
    'accounts',
    'hashtags',
    'bids',
    'notifications',
    'userstatistics',

    # third party stuff
    'crispy_forms',
    'rest_framework',
    'storages',
    # 'paypal.standard.ipn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # from django docs for setting the current session timezone
    'parties.middleware.TimezoneMiddleware',
]

# root url sets the main routing file. those then refer to the other url docs
ROOT_URLCONF = 'apogee1.urls'

# because login is built into django
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL

# Address of RabbitMQ instance, our Celery broker
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_BROKER_POOL_LIMIT = 8

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # this tells us where our html is coming from 
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'apogee1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
# sets the base url for our static serve
# it's currently local, but if we used AWS or something, we would send it there
STATIC_URL = '/static/'

# where our static files exist at the start
# will not be served, just long term storage
STATICFILES_DIRS = [
# BASE_DIR is the root of the django project
    os.path.join(BASE_DIR, "static-storage"),
]

# tells us where the static files exist at the end
# in production, this should be done by a cdn, not django
# will be served
STATIC_ROOT = os.path.join(BASE_DIR, "static-serve")


# this holds our media stuff like thumbnails and profile pics
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

# this just works with crispy form to render properly
CRISPY_TEMPLATE_PACK = 'bootstrap4'





