from .base import *

DEBUG = False

STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.StaticFilesStorage"

try:
    from .local import *
except ImportError:
    pass