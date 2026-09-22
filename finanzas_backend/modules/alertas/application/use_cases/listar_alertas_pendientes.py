"""Caso de uso: listar las alertas pendientes de un usuario."""

from dataclasses import dataclass

from modules.alertas.domain.entities import AlertaPago
from modules.alertas.domain.ports.repositories import AlertaPagoRepository


@dataclass
class ListarAlertasPendientesUseCase:
    repositorio: AlertaPagoRepository

    def ejecutar(self, usuario_id: int, estado: str = "Pendiente") -> list[AlertaPago]:
        """
        CONSIGNA: devolver las alertas del usuario en un estado dado
        (por defecto 'Pendiente'). Aprovecha idx_alertas_usuario_estado.
        El caso de uso solo orquesta.

        Retorno: list[AlertaPago]
        """
        return self.repositorio.listar_por_usuario_y_estado(usuario_id, estado)
