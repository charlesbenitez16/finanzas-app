"""
Puertos del dominio de alertas. Los implementa
infrastructure/repositories.py con Django ORM.
"""

from abc import ABC, abstractmethod
from typing import Optional

from modules.alertas.domain.entities import AlertaPago


class AlertaPagoRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, alerta_id: int) -> Optional[AlertaPago]:
        """Devuelve la AlertaPago con ese id, o None."""
        ...

    @abstractmethod
    def crear(self, alerta: AlertaPago) -> AlertaPago:
        """Persiste una AlertaPago nueva y la devuelve con id."""
        ...

    @abstractmethod
    def actualizar(self, alerta: AlertaPago) -> AlertaPago:
        """Persiste cambios de una AlertaPago existente (transiciones de estado)."""
        ...

    @abstractmethod
    def listar_por_usuario_y_estado(
        self, usuario_id: int, estado: str
    ) -> list[AlertaPago]:
        """
        MAPEO SQL -- aprovecha idx_alertas_usuario_estado
        (usuario_id, estado):
            SELECT * FROM alertas_pago
            WHERE usuario_id = %s AND estado = %s
            ORDER BY fecha_alerta

        Lo usa ListarAlertasPendientesUseCase (estado = 'Pendiente').
        """
        ...

    @abstractmethod
    def existe_alerta_para_servicio_en_periodo(
        self, servicio_fijo_id: int, periodo_mes: int, periodo_anio: int
    ) -> bool:
        """
        MAPEO SQL -- constraint uq_alerta_servicio_periodo:
            SELECT EXISTS(
                SELECT 1 FROM alertas_pago
                WHERE servicio_fijo_id = %s
                  AND periodo_anio = %s AND periodo_mes = %s
            )

        Lo usa GenerarAlertasDeVencimientoUseCase para no duplicar alertas.
        """
        ...

    @abstractmethod
    def obtener_por_servicio_y_periodo(
        self, servicio_fijo_id: int, periodo_mes: int, periodo_anio: int
    ) -> Optional[AlertaPago]:
        """
        MAPEO SQL -- misma clave unica que arriba, pero devolviendo la
        fila. Lo usa ResolverAlertaAlPagarUseCase (handler de
        GastoRegistrado) para encontrar la alerta que hay que resolver.
        """
        ...
