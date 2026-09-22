"""
Entidad de dominio del modulo alertas: AlertaPago.

Python puro (dataclass), sin Django. Mapea la tabla `alertas_pago` de
schema_finanzas.sql: recordatorios de vencimiento de servicios fijos,
con una maquina de estados Pendiente -> Enviada -> Leida -> Resuelta.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from modules.alertas.domain.exceptions import TransicionEstadoInvalida
from shared.domain.base_entity import Entity

ESTADOS_ALERTA = ("Pendiente", "Enviada", "Leida", "Resuelta")
_TRANSICIONES = {
        "Pendiente": {"Enviada"},
        "Enviada": {"Leida"},
        "Leida": set(),
        "Resuelta": set(),
    }

@dataclass
class AlertaPago(Entity):
    """
    Alerta de vencimiento de un servicio fijo para un periodo.

    CONSIGNA
    --------
    La entidad SI conoce su propia maquina de estados: los metodos
    marcar_*/resolver son transiciones que puede validar sola (solo
    miran self.estado). Que transiciones son legales:
        Pendiente -> Enviada -> Leida -> Resuelta
        (y "Resuelta" tambien se puede alcanzar desde cualquier estado
         no-resuelto cuando se paga el servicio).
    Una transicion ilegal debe lanzar TransicionEstadoInvalida.

    Campos (ver 01_schema.sql tabla `alertas_pago`):
        usuario_id       -- FK usuarios (NOT NULL)
        servicio_fijo_id -- FK servicios_fijos (NOT NULL)
        gasto_id         -- FK gastos, NULL hasta que se paga
        periodo_mes      -- SMALLINT 1..12
        periodo_anio     -- SMALLINT
        fecha_alerta     -- cuando toca avisar
        estado           -- ESTADOS_ALERTA
        mensaje          -- texto para el usuario
    """

    usuario_id: Optional[int] = None
    servicio_fijo_id: Optional[int] = None
    gasto_id: Optional[int] = None
    periodo_mes: int = 0
    periodo_anio: int = 0
    fecha_alerta: Optional[date] = None
    estado: str = "Pendiente"
    mensaje: Optional[str] = None
    fecha_creacion: Optional[datetime] = None


    def esta_pendiente(self) -> bool:
        """CONSIGNA: True si estado == 'Pendiente'. Retorno: bool."""
        return self.estado == "Pendiente"

    def esta_resuelta(self) -> bool:
        """CONSIGNA: True si estado == 'Resuelta'. Retorno: bool."""
        return self.estado == "Resuelta"

    def _transicionar(self, nuevo: str) -> None:
        if nuevo not in _TRANSICIONES.get(self.estado, set()):
            raise TransicionEstadoInvalida(
                f"No se puede pasar de {self.estado} a {nuevo}")
        self.estado = nuevo

    def marcar_enviada(self) -> None:
        """
        CONSIGNA: transicion Pendiente -> Enviada. Si el estado actual no
        lo permite, lanzar TransicionEstadoInvalida.

        Retorno: None (muta self.estado)
        """
        self._transicionar("Enviada")

    def marcar_leida(self) -> None:
        """
        CONSIGNA: transicion Enviada -> Leida. Si el estado actual no lo
        permite, lanzar TransicionEstadoInvalida.
        """
        self._transicionar("Leida")

    def resolver(self, gasto_id: int) -> None:
        """
        CONSIGNA: se llama cuando el usuario paga el servicio. Setea
        self.gasto_id y pasa el estado a 'Resuelta'. Solo tiene sentido
        si la alerta no estaba ya resuelta (si lo estaba: decidi si es
        no-op o TransicionEstadoInvalida).

        Params: gasto_id (int) -- el Gasto que resolvio esta alerta
        Retorno: None
        """
        if self.esta_resuelta():
            return                       # idempotente: el evento puede llegar 2 veces
        self.gasto_id = gasto_id
        self.estado = "Resuelta"

    def es_estado_valido(self) -> bool:
        """CONSIGNA: replica el CHECK del schema: estado in ESTADOS_ALERTA."""
        return self.estado in ESTADOS_ALERTA
