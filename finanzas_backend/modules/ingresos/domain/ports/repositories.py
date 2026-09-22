"""
Puertos del dominio de ingresos. Los implementa
infrastructure/repositories.py con Django ORM; el dominio y la aplicacion
solo dependen de estas interfaces abstractas.
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional

from modules.ingresos.domain.entities import Ingreso


class IngresoRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, ingreso_id: int) -> Optional[Ingreso]:
        """Devuelve el Ingreso con ese id, o None."""
        ...

    @abstractmethod
    def crear(self, ingreso: Ingreso) -> Ingreso:
        """Persiste un Ingreso nuevo y lo devuelve con id."""
        ...

    @abstractmethod
    def listar_por_usuario_y_periodo(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> list[Ingreso]:
        """
        Todos los ingresos de un usuario en un periodo, ordenados por fecha.
        Aprovecha idx_ingresos_usuario_periodo (usuario_id, periodo_anio,
        periodo_mes).

        MAPEO SQL:
            SELECT * FROM ingresos
            WHERE usuario_id = %s AND periodo_anio = %s AND periodo_mes = %s
            ORDER BY fecha
        """
        ...

    @abstractmethod
    def sumar_montos_por_periodo(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> Decimal:
        """
        MAPEO SQL -- lado "ingresos" de vista_balance_mensual:
            SELECT COALESCE(SUM(monto), 0)
            FROM ingresos
            WHERE usuario_id = %s AND periodo_anio = %s AND periodo_mes = %s

        Retorno: Decimal (0 si el usuario no tuvo ingresos ese mes).
        """
        ...
