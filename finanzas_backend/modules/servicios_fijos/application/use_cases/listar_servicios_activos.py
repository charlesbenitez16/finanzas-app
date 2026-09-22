"""Caso de uso: listar los servicios fijos activos de un usuario."""

from dataclasses import dataclass

from modules.servicios_fijos.domain.entities import ServicioFijo
from modules.servicios_fijos.domain.ports.repositories import ServicioFijoRepository


@dataclass
class ListarServiciosActivosUseCase:
    repositorio: ServicioFijoRepository

    def ejecutar(self, usuario_id: int) -> list[ServicioFijo]:
        """
        CONSIGNA: devolver los servicios fijos del usuario con activo =
        TRUE, ordenados por nombre. El caso de uso solo orquesta (mismo
        estilo que ListarCategoriasUseCase en catalogos).

        Retorno: list[ServicioFijo]
        """
        return self.repositorio.listar_por_usuario(usuario_id, solo_activos=True)
