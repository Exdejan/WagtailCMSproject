import os
import sys
import urllib.parse
from pathlib import Path

# ✅ CLOUDINARY IMPORTS (moved to top)
import cloudinary
import cloudinary.uploader
import cloudinary.api

PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_DIR.parent

# SECURITY (important for deployment later)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://ourfavorites.up.railway.app",
]

# Application definition
INSTALLED_APPS = [
    "home",
    "search",
    "cloudinary_storage",
    "cloudinary",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django_filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "CMS.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "CMS.wsgi.application"

# ✅ DATABASE DEBUG + CONFIG
print(">>> DJANGO_SETTINGS_MODULE =", os.environ.get("DJANGO_SETTINGS_MODULE"), file=sys.stderr)
print(">>> DATABASE_URL =", os.environ.get("DATABASE_URL"), file=sys.stderr)

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    parsed = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path[1:],
            "USER": parsed.username,
            "PASSWORD": parsed.password,
            "HOST": parsed.hostname,
            "PORT": parsed.port,
            "CONN_MAX_AGE": 600,
        }
    }
    print(f">>> DB HOST={parsed.hostname} NAME={parsed.path[1:]} USER={parsed.username}", file=sys.stderr)

    # Test raw psycopg2 connection
    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port,
        )
        conn.close()
        print(">>> PSYCOPG2 CONNECTION: SUCCESS", file=sys.stderr)
    except Exception as e:
        print(f">>> PSYCOPG2 CONNECTION FAILED: {type(e).__name__}: {e}", file=sys.stderr)

else:
    print(">>> ⚠️ DATABASE_URL is MISSING — falling back to SQLite!", file=sys.stderr)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# ✅ CLOUDINARY CONFIGURATION
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET')
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

# Wagtail
WAGTAIL_SITE_NAME = "CMS"

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

WAGTAILADMIN_BASE_URL = "https://ourfavorites.up.railway.app"

WAGTAILDOCS_EXTENSIONS = [
    'csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip'
]

print(">>> FINAL DATABASES ENGINE =", DATABASES['default'].get('ENGINE', 'MISSING'), file=sys.stderr)