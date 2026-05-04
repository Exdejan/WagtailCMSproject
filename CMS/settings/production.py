from .base import *

DEBUG = False

# ✅ Use WhiteNoise for static files (Cloudinary handles media)
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# ✅ Comment out the old manifest storage override
# STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

try:
    from .local import *
except ImportError:
    pass