"""Configuracion para produccion."""

import os

from .base import *  # noqa: F401,F403

DEBUG = False
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

CORS_ALLOWED_ORIGINS = [
        origin for origin in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if origin
    ]
CSRF_TRUSTED_ORIGINS = [
        origin for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if origin
    ]
