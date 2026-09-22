"""
Configuracion base de Django, compartida por dev.py y prod.py.
Los valores sensibles (SECRET_KEY, credenciales de base de datos) se leen
desde variables de entorno para no versionarlos en el repositorio.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-cambiame-en-produccion",
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    # Modulos de la aplicacion (bounded contexts del monolito modular)
    "modules.catalogos",
    "modules.usuarios",
    "modules.ingresos",
    "modules.servicios_fijos",
    "modules.gastos",
    "modules.planes_financieros",
    "modules.alertas",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Base de datos: misma instancia Postgres de docker-compose.yml.
# Sobreescribe con variables de entorno si tu configuracion difiere.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "finanzas_db"),
        "USER": os.environ.get("POSTGRES_USER", "finanzas_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "finanzas_pass"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django busca migraciones en <app>/migrations/ por defecto. Como las
# nuestras viven en infrastructure/migrations/ (arquitectura hexagonal),
# hay que decirselo explicitamente aca, una entrada por modulo.
MIGRATION_MODULES = {
    "catalogos": "modules.catalogos.infrastructure.migrations",
    "usuarios": "modules.usuarios.infrastructure.migrations",
    "ingresos": "modules.ingresos.infrastructure.migrations",
    "servicios_fijos": "modules.servicios_fijos.infrastructure.migrations",
    "gastos": "modules.gastos.infrastructure.migrations",
    "planes_financieros": "modules.planes_financieros.infrastructure.migrations",
    "alertas": "modules.alertas.infrastructure.migrations",
}

REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            # JWT primero: es lo que va a usar el frontend (Authorization:
            # Bearer <access>). Session/Basic quedan de respaldo para
            # probar a mano (Swagger, curl, /admin/).
            "rest_framework_simplejwt.authentication.JWTAuthentication",
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.BasicAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }

from datetime import timedelta  # noqa: E402

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# drf-spectacular: genera el esquema OpenAPI a partir de las vistas/
# serializers y lo sirve en /api/schema/, con Swagger UI en /api/docs/
# y ReDoc en /api/redoc/ (rutas registradas en config/urls.py).
SPECTACULAR_SETTINGS = {
    "TITLE": "Finanzas API",
    "DESCRIPTION": (
        "API del sistema de finanzas personales: usuarios, ingresos, "
        "servicios fijos, gastos, planes financieros y alertas de pago."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/",
}

EMAIL_BACKEND = os.environ.get(
        "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
    )
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "no-reply@finanzas.local")