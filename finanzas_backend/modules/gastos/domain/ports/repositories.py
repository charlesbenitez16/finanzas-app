"""
Puertos del dominio de gastos. Los implementa
infrastructure/repositories.py con Django ORM. Aca estan la mayoria de
las consultas del schema (vistas A, B, C y varias constraints).
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional

from modules.gastos.domain.entities import AhorroPorPrioridad, Gasto


class GastoRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, gasto_id: int) -> Optional[Gasto]:
        """Devuelve el Gasto con ese id, o None."""
        ...

    @abstractmethod
    def crear(self, gasto: Gasto) -> Gasto:
        """Persiste un Gasto nuevo y lo devuelve con id."""
        ...

    @abstractmethod
    def listar_por_usuario_y_periodo(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> list[Gasto]:
        """
        Aprovecha idx_gastos_usuario_periodo.

        MAPEO SQL:
            SELECT * FROM gastos
            WHERE usuario_id = %s AND periodo_anio = %s AND periodo_mes = %s
            ORDER BY fecha_gasto
        """
        ...

    @abstractmethod
    def sumar_montos_por_periodo(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> Decimal:
        """
        MAPEO SQL -- lado "gastos" de vista_balance_mensual:
            SELECT COALESCE(SUM(monto), 0)
            FROM gastos
            WHERE usuario_id = %s AND periodo_anio = %s AND periodo_mes = %s

        Retorno: Decimal (0 si no hubo gastos ese mes).
        """
        ...

    @abstractmethod
    def existe_pago_de_servicio_en_periodo(
        self, servicio_fijo_id: int, periodo_mes: int, periodo_anio: int
    ) -> bool:
        """
        MAPEO SQL -- constraint uq_gasto_servicio_periodo ("evita registrar
        dos veces el mismo servicio fijo en el mismo periodo"):
            SELECT EXISTS(
                SELECT 1 FROM gastos
                WHERE servicio_fijo_id = %s
                  AND periodo_anio = %s AND periodo_mes = %s
            )

        Lo usa RegistrarPagoDeServicioFijoUseCase antes de insertar.
        """
        ...

    @abstractmethod
    def listar_pagos_de_servicio_fijo(
        self, servicio_fijo_id: int
    ) -> list[Gasto]:
        """
        MAPEO SQL -- insumo de vista_variacion_servicios. Todos los pagos
        de un servicio fijo, ORDENADOS por (periodo_anio, periodo_mes),
        para poder calcular la variacion mes a mes (el LAG de la vista):
            SELECT * FROM gastos
            WHERE servicio_fijo_id = %s
            ORDER BY periodo_anio, periodo_mes
        """
        ...

    @abstractmethod
    def total_por_prioridad(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> list[AhorroPorPrioridad]:
        """
        MAPEO SQL -- vista_ahorro_potencial_por_prioridad:
            SELECT np.nombre, np.nivel_orden, SUM(g.monto)
            FROM gastos g
            JOIN niveles_prioridad np ON np.id = g.prioridad_id
            WHERE g.usuario_id = %s AND g.periodo_anio = %s AND g.periodo_mes = %s
            GROUP BY np.nombre, np.nivel_orden
            ORDER BY np.nivel_orden

        Retorno: list[AhorroPorPrioridad] (ordenada por nivel_orden).
        """
        ...
