"""Caso de uso: registrar un gasto puntual (NO ligado a un servicio fijo)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from modules.gastos.domain.entities import ESTADOS_GASTO, Gasto
from modules.gastos.domain.exceptions import EstadoGastoInvalido, MontoInvalido
from modules.gastos.domain.ports.repositories import GastoRepository

from shared.domain.events import event_bus
from modules.gastos.domain.events import GastoRegistrado

@dataclass
class RegistrarGastoUseCase:
    """
    CONSIGNA
    --------
    Alta de un gasto puntual (mercado, salidas, compras varias):
    servicio_fijo_id queda en None.
      1. monto > 0                 -> si no, MontoInvalido
      2. estado valido             -> si no, EstadoGastoInvalido
      3. construir Gasto (sin id, servicio_fijo_id=None) y persistir.
      4. publicar GastoRegistrado en el event_bus (shared/domain/events.py)
         para que `alertas` pueda reaccionar. Para un gasto puntual
         servicio_fijo_id=None: la alerta no hace nada, pero mantene la
         publicacion uniforme.

    Params de ejecutar(): usuario_id, categoria_id, prioridad_id, monto,
        fecha_gasto, periodo_mes, periodo_anio, estado, descripcion
    Retorno: Gasto (con id)
    """

    repositorio: GastoRepository

    def ejecutar(
        self,
        usuario_id: int,
        categoria_id: int,
        prioridad_id: int,
        monto: Decimal,
        fecha_gasto: date,
        periodo_mes: int,
        periodo_anio: int,
        estado: str = "Pagado",
        descripcion: Optional[str] = None,
    ) -> Gasto:
        if monto is None or monto <= 0:
            raise MontoInvalido("El monto debe ser mayor a 0")
        if estado not in ESTADOS_GASTO:
            raise EstadoGastoInvalido(f"Estado invalido: {estado}")
        gasto = Gasto(
            usuario_id=usuario_id, categoria_id=categoria_id, servicio_fijo_id=None,
            prioridad_id=prioridad_id, monto=monto, fecha_gasto=fecha_gasto,
            periodo_mes=periodo_mes, periodo_anio=periodo_anio, estado=estado,
            descripcion=descripcion,
        )
        gasto = self.repositorio.crear(gasto)
        event_bus.publicar(GastoRegistrado(
            gasto_id=gasto.id, usuario_id=gasto.usuario_id, servicio_fijo_id=None,
            periodo_mes=gasto.periodo_mes, periodo_anio=gasto.periodo_anio,
        ))
        return gasto
