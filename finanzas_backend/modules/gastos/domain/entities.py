"""
Dominio del modulo gastos.

Contiene:
  - Gasto            -> entidad (hereda de Entity), mapea la tabla `gastos`.
  - BalanceMensual   -> objeto de LECTURA (no se persiste): resultado de
                        vista_balance_mensual.
  - VariacionServicio-> objeto de LECTURA: fila de vista_variacion_servicios.
  - AhorroPorPrioridad-> objeto de LECTURA: fila de
                        vista_ahorro_potencial_por_prioridad.

Los tres objetos de lectura son dataclasses simples (NO heredan de
Entity, no tienen id, no van al repositorio como entidades). Van juntos
aca por simplicidad; si el modulo crece, movelos a domain/read_models.py.
Todo Python puro, sin Django.
"""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from shared.domain.base_entity import Entity

ESTADOS_GASTO = ("Pagado", "Pendiente", "Vencido")


@dataclass
class Gasto(Entity):
    """
    Una transaccion real de gasto: puede ser el pago de un servicio fijo
    (servicio_fijo_id != None) o un gasto puntual (mercado, salidas...).

    CONSIGNA
    --------
    Metodos = solo lo que el Gasto resuelve con sus propios atributos.
    Sumar, comparar contra otros gastos o contra el plan: eso vive en
    casos de uso, no aca.

    Campos (ver 01_schema.sql tabla `gastos`):
        usuario_id       -- FK usuarios (NOT NULL)
        categoria_id     -- FK categorias_gasto (NOT NULL)
        servicio_fijo_id -- FK servicios_fijos, NULL si es gasto no recurrente
        prioridad_id     -- FK niveles_prioridad (NOT NULL)
        monto            -- NUMERIC(12,2), CHECK (monto > 0)
        fecha_gasto      -- fecha real
        periodo_mes      -- SMALLINT 1..12
        periodo_anio     -- SMALLINT
        estado           -- 'Pagado' | 'Pendiente' | 'Vencido'
        descripcion      -- texto libre
    """

    usuario_id: Optional[int] = None
    categoria_id: Optional[int] = None
    servicio_fijo_id: Optional[int] = None
    prioridad_id: Optional[int] = None
    monto: Decimal = Decimal("0")
    fecha_gasto: Optional[date] = None
    periodo_mes: int = 0
    periodo_anio: int = 0
    estado: str = "Pagado"
    descripcion: Optional[str] = None
    fecha_registro: Optional[datetime] = None

    def es_pago_de_servicio_fijo(self) -> bool:
        """CONSIGNA: True si este gasto esta ligado a un servicio fijo. Retorno: bool."""
        return self.servicio_fijo_id is not None

    def esta_pagado(self) -> bool:
        """CONSIGNA: True si estado == 'Pagado'. Retorno: bool."""
        return self.estado == "Pagado"

    def pertenece_al_periodo(self, mes: int, anio: int) -> bool:
        """CONSIGNA: True si (periodo_mes, periodo_anio) == (mes, anio). Retorno: bool."""
        return self.periodo_mes == mes and self.periodo_anio == anio

    def es_estado_valido(self) -> bool:
        """CONSIGNA: replica el CHECK del schema: estado in ESTADOS_GASTO. Retorno: bool."""
        return self.estado in ESTADOS_GASTO


@dataclass
class BalanceMensual:
    """
    Objeto de lectura -- resultado de vista_balance_mensual para un
    usuario y periodo:
        balance = total_ingresos - total_gastos
    """

    usuario_id: int
    periodo_mes: int
    periodo_anio: int
    total_ingresos: Decimal
    total_gastos: Decimal
    balance: Decimal


@dataclass
class VariacionServicio:
    """
    Objeto de lectura -- fila de vista_variacion_servicios: cuanto vario
    el monto de un servicio fijo respecto al mes anterior.
        porcentaje_variacion = (actual - anterior) / anterior * 100
    `monto_anterior` y `porcentaje_variacion` son None en el primer
    periodo con datos (no hay contra que comparar).
    """

    servicio_fijo_id: int
    servicio: str
    periodo_mes: int
    periodo_anio: int
    monto_actual: Decimal
    monto_anterior: Optional[Decimal]
    porcentaje_variacion: Optional[Decimal]


@dataclass
class AhorroPorPrioridad:
    """
    Objeto de lectura -- fila de vista_ahorro_potencial_por_prioridad:
    cuanto gasta el usuario en un periodo agrupado por nivel de prioridad.
    Sirve para la simulacion de "modo emergencia" (cuanto se ahorraria si
    se suspenden los gastos de tal prioridad hacia abajo).
    """

    prioridad: str
    nivel_orden: int
    total_por_prioridad: Decimal


@dataclass
class AhorroEmergencia:
        """Fila del simulador: cuánto se ahorra suspendiendo esta prioridad
        y todas las MÁS prescindibles que ella."""
        prioridad: str
        nivel_orden: int
        total_periodo: Decimal
        ahorro_acumulado_si_suspende: Decimal
