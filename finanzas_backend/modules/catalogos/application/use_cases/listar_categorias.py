"""Caso de uso: listar las categorias de gasto disponibles para un usuario."""

from dataclasses import dataclass

from modules.catalogos.domain.entities import CategoriaGasto
from modules.catalogos.domain.ports.repositories import CategoriaGastoRepository


@dataclass
class ListarCategoriasUseCase:
    """
    El repositorio se recibe por inyeccion de dependencias: este caso de
    uso no sabe si detras hay Django ORM, otra base de datos, o una lista
    en memoria para un test.
    """

    repositorio: CategoriaGastoRepository

    def ejecutar(self, usuario_id: int) -> list[CategoriaGasto]:
        # El repositorio ya se encarga de traer globales + personalizadas
        # (ver el docstring del puerto en domain/ports/repositories.py).
        # El caso de uso queda deliberadamente fino: orquesta, no decide.
        return self.repositorio.listar_para_usuario(usuario_id)
