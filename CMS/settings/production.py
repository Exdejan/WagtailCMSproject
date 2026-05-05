from .base import *
import os
import dj_database_url

DEBUG = False

# Database - pulls from Railway's DATABASE_URL environment variable
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )
}

# Allowed hosts - reads from environment variable
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'ourfavorites.up.railway.app').split(',')

# CSRF trusted origins - required for Wagtail admin to work properly
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'https://ourfavorites.up.railway.app'
).split(',')

# Secret key - reads from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'unsafe-secret-key-replace-this')

# Static files - Whitenoise for serving static files in production
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Whitenoise middleware should already be in base.py, but double-check
# it's placed right after SecurityMiddleware in MIDDLEWARE

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/6.0/ref/contrib/staticfiles/#manifeststaticfilesstorage

try:
    from .local import *
except ImportError:
    pass