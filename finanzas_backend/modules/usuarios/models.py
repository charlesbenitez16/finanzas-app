"""
Django exige que los modelos esten en <app>/models.py para poder
descubrirlos (migraciones, admin, etc.). Los modelos reales viven en
infrastructure/models.py para respetar la arquitectura hexagonal; este
archivo solo los re-exporta para que Django los encuentre donde los
busca por convencion. No hace falta tocar este archivo.
"""

from modules.usuarios.infrastructure.models import UsuarioModel  # noqa: F401
