from .base import *

DEBUG = False

STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedStaticFilesStorage"

try:
    from .local import *
except ImportError:
    pass