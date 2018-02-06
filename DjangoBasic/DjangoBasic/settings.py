"""
Django settings for DjangoBasic project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q*!m@qyqm$=#%0(j5&!!4_ew=((0q8bbqh_g#yola-!rzkgt_@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
# all application defined by developer should be added to the list below manually
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Book',
]

# customized middleware registered here
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # customized middleware, for automatic cookie setting
    'Book.middleware.CookieSetMiddleware'
]

ROOT_URLCONF = 'DjangoBasic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # the path that used to mark the templates folder, in which all templates should be stored
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'DjangoBasic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# All information for database connection should be added in the dictionary shown below
# the default choice is Sqlite, a lightweight relational database which are used as builtin database of python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '123456'
    }
}


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

# For changing time zone and language code
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/')

# configuration for logging part
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'special': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {},
    'handlers': {
        'file_handler': {
            'level': 'DEBUG',
            'class': 'logging.TimedRotatingFileHandler',
            'filename': 'basic_log.log',

        },
        'console': {
            'level': 'INFO',
            'filters': ['special'],
            'class': 'logging.StreamHandler',

        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['console', 'file_handler'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
