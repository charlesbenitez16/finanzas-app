"""
Dominio del modulo planes_financieros.

Contiene:
  - PlanFinanciero        -> entidad (hereda de Entity), mapea la tabla
                             `plan_financiero`.
  - ComparativaPlanVsReal -> objeto de LECTURA (no se persiste): resultado
                             de vista_plan_vs_real.

Python puro, sin Django.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional

from shared.domain.base_entity import Entity
from decimal import Decimal, ROUND_HALF_UP


@dataclass
class PlanFinanciero(Entity):
    """
    Plan de reparto del ingreso, estilo 50/30/20 pero personalizable
    (gasto fijo / ahorro / gasto libre).

    CONSIGNA
    --------
    A diferencia de NivelPrioridad (que NO podia decidir sola si era "la
    mas baja"), este plan SI puede validar su propia invariante: los tres
    porcentajes son atributos suyos y su suma debe dar 100 (CHECK del
    schema). Ese metodo va aca. Comparar contra la ejecucion real de un
    mes, en cambio, necesita datos de ingresos/gastos: eso es un caso de
    uso.

    Campos (ver 01_schema.sql tabla `plan_financiero`):
        usuario_id             -- FK usuarios (NOT NULL)
        nombre                 -- 'Mi plan' por defecto
        porcentaje_gasto_fijo  -- NUMERIC(5,2) >= 0
        porcentaje_ahorro      -- NUMERIC(5,2) >= 0
        porcentaje_gasto_libre -- NUMERIC(5,2) >= 0
        fecha_inicio           -- desde cuando rige
        fecha_fin              -- hasta cuando (None = sin fin)
        activo                 -- solo uno activo por usuario (uq_plan_activo_usuario)
    """

    usuario_id: Optional[int] = None
    nombre: str = "Mi plan"
    porcentaje_gasto_fijo: Decimal = Decimal("0")
    porcentaje_ahorro: Decimal = Decimal("0")
    porcentaje_gasto_libre: Decimal = Decimal("0")
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    activo: bool = True

    def porcentajes_suman_100(self) -> bool:
        """
        CONSIGNA: replica el CHECK
        (porcentaje_gasto_fijo + porcentaje_ahorro + porcentaje_gasto_libre = 100).

        Retorno: bool
        """
        suma = (self.porcentaje_gasto_fijo + self.porcentaje_ahorro
                + self.porcentaje_gasto_libre)
        return suma == Decimal("100")

    def esta_activo(self) -> bool:
        """CONSIGNA: lectura directa del flag `activo`. Retorno: bool."""
        return self.activo

    def esta_vigente(self, fecha: date) -> bool:
        """
        CONSIGNA: True si `fecha` cae dentro de [fecha_inicio, fecha_fin]
        (fecha_fin None = sin limite).

        Retorno: bool
        """
        if self.fecha_inicio and fecha < self.fecha_inicio:
            return False
        if self.fecha_fin and fecha > self.fecha_fin:
            return False
        return True

    def _meta(self, ingreso_total: Decimal, porcentaje: Decimal) -> Decimal:
        return (ingreso_total * porcentaje / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP)

    def meta_gasto_fijo(self, ingreso_total: Decimal) -> Decimal:
        """
        CONSIGNA: monto objetivo de gasto fijo para un ingreso dado:
            ingreso_total * porcentaje_gasto_fijo / 100
        (redondeado a 2 decimales, como ROUND(..., 2) en vista_plan_vs_real).

        Retorno: Decimal
        """
        return self._meta(ingreso_total, self.porcentaje_gasto_fijo)

    def meta_ahorro(self, ingreso_total: Decimal) -> Decimal:
        """CONSIGNA: idem meta_gasto_fijo pero con porcentaje_ahorro. Retorno: Decimal."""
        return self._meta(ingreso_total, self.porcentaje_ahorro)

    def meta_gasto_libre(self, ingreso_total: Decimal) -> Decimal:
        """CONSIGNA: idem pero con porcentaje_gasto_libre. Retorno: Decimal."""
        return self._meta(ingreso_total, self.porcentaje_gasto_libre)


@dataclass
class ComparativaPlanVsReal:
    """
    Objeto de lectura -- fila de vista_plan_vs_real: mete/real de un mes.
    """

    usuario_id: int
    periodo_mes: int
    periodo_anio: int
    total_ingresos: Decimal
    meta_gasto_fijo: Decimal
    meta_ahorro: Decimal
    meta_gasto_libre: Decimal
    gasto_real: Decimal
    balance_real: Decimal
