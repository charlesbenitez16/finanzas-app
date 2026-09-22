"""
Eventos de dominio que publica el modulo gastos.

El bus vive en shared/domain/events.py. modules/alertas se suscribe a
GastoRegistrado para marcar como 'Resuelta' la alerta del servicio fijo
que se acaba de pagar (ver el docstring de shared/domain/events.py).
"""

from dataclasses import dataclass
from typing import Optional

from shared.domain.events import DomainEvent


@dataclass(frozen=True)
class GastoRegistrado(DomainEvent):
    """
    CONSIGNA: se publica cuando se registra un gasto (puntual o pago de
    servicio fijo). El suscriptor de `alertas` lo usa para encontrar la
    alerta correspondiente, asi que lleva lo minimo para eso: usuario,
    servicio fijo (si aplica) y periodo.

    Campos:
        gasto_id         -- id del Gasto recien creado
        usuario_id       -- dueno del gasto
        servicio_fijo_id -- None si fue un gasto puntual
        periodo_mes / periodo_anio -- periodo del gasto
    """

    gasto_id: int = 0
    usuario_id: int = 0
    servicio_fijo_id: Optional[int] = None
    periodo_mes: int = 0
    periodo_anio: int = 0
