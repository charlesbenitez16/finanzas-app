"""
Puertos (interfaces) que el dominio de usuarios necesita del exterior.

Quien los implementa es infrastructure/repositories.py con Django ORM,
pero el dominio y la aplicacion nunca dependen de esa implementacion:
solo dependen de esta interfaz abstracta. Esto es lo que permite testear
los casos de uso sin tocar la base de datos (ver tests/application/).
"""

from abc import ABC, abstractmethod
from typing import Optional

from modules.usuarios.domain.entities import Usuario


class UsuarioRepository(ABC):
    """
    CONSIGNA: contrato de persistencia para Usuario. Defini SOLO lo que
    los casos de uso de este modulo necesitan, nada mas.
    """

    @abstractmethod
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Devuelve el Usuario con ese id, o None si no existe."""
        ...

    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """
        Devuelve el Usuario con ese email (comparacion case-insensitive),
        o None.

        MAPEO SQL:
            SELECT * FROM usuarios WHERE lower(email) = lower(%s)
        """
        ...

    @abstractmethod
    def existe_email(self, email: str) -> bool:
        """
        True si ya hay un usuario con ese email. Lo usa
        RegistrarUsuarioUseCase para no chocar con usuarios.email UNIQUE.

        MAPEO SQL:
            SELECT EXISTS(SELECT 1 FROM usuarios WHERE lower(email) = lower(%s))
        """
        ...

    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        """Persiste un Usuario nuevo y lo devuelve ya con id asignado."""
        ...

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        """Persiste cambios de un Usuario existente (ej. baja logica)."""
        ...
