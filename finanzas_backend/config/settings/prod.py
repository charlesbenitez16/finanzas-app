"""Configuracion para produccion."""

import os

from .base import *  # noqa: F401,F403

DEBUG = False
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")

# TODO antes de desplegar a produccion:
# - SECRET_KEY debe venir de una variable de entorno segura (no el valor por defecto de base.py)
# - Configurar HTTPS: SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE
# - Configurar STATIC_ROOT y correr collectstatic
