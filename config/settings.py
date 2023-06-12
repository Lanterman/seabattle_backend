"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import logging

from pathlib import Path
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")
logging.basicConfig(format="[%(asctime)s] | %(levelname)s: %(message)s", level=logging.INFO, datefmt='%m.%d.%Y %H:%M:%S')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DOC_SECRET_KEY", os.environ["SECRET_KEY"])

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DOC_DEBUG", os.environ["DEBUG"]))

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = bool(os.getenv("DOC_CORS_ORIGIN_ALLOW_ALL", os.environ["CORS_ORIGIN_ALLOW_ALL"]))
# CORS_ORIGIN_WHITELIST = (os.getenv("DOC_CORS_ORIGIN_WHITELIST", os.environ["CORS_ORIGIN_WHITELIST"]),)

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'channels',
    'corsheaders',
    'debug_toolbar',
    'django_filters',
    'drf_yasg',

    'src.game.apps.GameConfig',
    'src.user.apps.UserConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

# WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DOC_ENGINE', os.environ['ENGINE_DB']),
        'NAME': os.environ.get('DOC_NAME', os.environ['NAME_DB']),
        'USER': os.environ.get('DOC_USER', os.environ['USER_DB']),
        'PASSWORD': os.environ.get('DOC_PASSWORD', os.environ['PASSWORD_DB']),
        'HOST': os.environ.get('DOC_HOST_DB', os.environ['HOST_DB']),
        'PORT': os.environ.get('DOC_PORT_DB', os.environ['PORT_DB']),

        'TEST': {'NAME': os.path.join(BASE_DIR, "test_db")}
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('DOC_HOST_CL', os.environ['HOST_DB']), 6379)],
            "group_expiry": 10800,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATETIME_FORMAT = "d.m.Y G:i:s"

DATETIME_INPUT_FORMATS = ["d.m.Y G:i:s"]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
        ),
    #     'rest_framework.authentication.TokenAuthentication',
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'user': '2/min'
    # },
    # 'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ('v1',),
    'DATETIME_FORMAT': '%d.%m.%Y %H:%M:%S',
    'DATETIME_INPUT_FORMATS': '%d.%m.%Y %H:%M:%S',
    'COMPACT_JSON': False,
}

INTERNAL_IPS = [
    '127.0.0.1',
    '0.0.0.0'
]

LOGIN_REDIRECT_URL = "/api/v1/"

AUTH_USER_MODEL = "user.User"

REDIS_HOST = os.environ.get('DOC_HOST_CL', os.environ['REDIS_HOST'])
REDIS_PORT = 6379
REDIS_PASSWORD = os.environ.get('DOC_REDIS_PASSWORD', os.environ['REDIS_PASSWORD'])

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_RESULT_EXPIRES = 3
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True