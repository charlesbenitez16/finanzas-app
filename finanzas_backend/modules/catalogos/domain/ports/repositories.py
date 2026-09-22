"""
Puertos (interfaces) que el dominio de catalogos necesita del exterior.

Quien los implementa es infrastructure/repositories.py con Django ORM,
pero el dominio y la aplicacion nunca dependen de esa implementacion:
solo dependen de esta interfaz abstracta. Esto es lo que permite testear
los casos de uso sin tocar la base de datos.
"""

from abc import ABC, abstractmethod
from typing import Optional

from modules.catalogos.domain.entities import CategoriaGasto, NivelPrioridad


class CategoriaGastoRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, categoria_id: int) -> Optional[CategoriaGasto]:
        ...

    @abstractmethod
    def listar_para_usuario(self, usuario_id: int) -> list[CategoriaGasto]:
        """Debe devolver las categorias globales + las personalizadas del usuario."""
        ...

    @abstractmethod
    def crear(self, categoria: CategoriaGasto) -> CategoriaGasto:
        ...


class NivelPrioridadRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, nivel_id: int) -> Optional[NivelPrioridad]:
        ...

    @abstractmethod
    def listar_todos(self) -> list[NivelPrioridad]:
        """Debe devolver todos los niveles ordenados por nivel_orden."""
        ...
