"""Configuracion para desarrollo local."""

from .base import *  # noqa: F401,F403

DEBUG = False
# "0.0.0.0" hace falta porque runserver escucha en todas las interfaces
# dentro del contenedor; si accedes con esa misma direccion en el
# navegador, el header Host que llega es literalmente "0.0.0.0:8000".
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
