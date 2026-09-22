"""Clase base para las entidades de dominio de todos los modulos."""

from abc import ABC
from dataclasses import dataclass
from typing import Optional


@dataclass
class Entity(ABC):
    """
    Base para toda entidad de dominio. Solo conoce su id: nada de Django,
    nada de framework. Cada modulo define sus propias entidades heredando
    de esta clase.
    """

    id: Optional[int] = None

    def es_nueva(self) -> bool:
        """True si la entidad todavia no fue persistida (no tiene id)."""
        return self.id is None
