"""Caso de uso: listar los niveles de prioridad disponibles."""

from dataclasses import dataclass

from modules.catalogos.domain.entities import NivelPrioridad
from modules.catalogos.domain.ports.repositories import NivelPrioridadRepository


@dataclass
class ListarNivelesPrioridadUseCase:
    repositorio: NivelPrioridadRepository

    def ejecutar(self) -> list[NivelPrioridad]:
        # El contrato del puerto (ver domain/ports/repositories.py) ya
        # promete que devuelve la lista ordenada por nivel_orden, asi que
        # el caso de uso no tiene nada mas que orquestar aca.
        return self.repositorio.listar_todos()
