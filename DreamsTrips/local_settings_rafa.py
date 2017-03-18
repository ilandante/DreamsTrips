# -*- coding: utf-8 -*-
from .settings import *
__author__ = 'rafa'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dreams_db',
        'USER': 'root',
        'PASSWORD': 'fadetoblack13',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True
    }
}

ALLOWED_HOSTS = []

STATIC_ROOT = ''


STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates/static/'),
)


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PRODUCTION = False

DEBUG = True

# STATIC_URL = '/static/'
MEDIA_URL = '/media/'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "rmoreno.ter@gmail.com"
EMAIL_HOST_PASSWORD = "fadetoblack13"
EMAIL_PORT = 587


