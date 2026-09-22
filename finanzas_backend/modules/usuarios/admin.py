"""
Igual que con models.py: Django busca el admin en <app>/admin.py.
El admin real vive en infrastructure/admin.py; esto solo lo importa para
que se registre. No hace falta tocar este archivo.
"""

from modules.usuarios.infrastructure.admin import *  # noqa: F401,F403
