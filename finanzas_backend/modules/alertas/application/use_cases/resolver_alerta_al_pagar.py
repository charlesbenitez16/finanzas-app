"""Caso de uso / handler: resolver la alerta cuando se registra el pago del servicio."""

from dataclasses import dataclass

from modules.alertas.domain.ports.repositories import AlertaPagoRepository
from modules.gastos.domain.events import GastoRegistrado
import logging
logger = logging.getLogger(__name__)


@dataclass
class ResolverAlertaAlPagarUseCase:
    """
    CONSIGNA
    --------
    Suscriptor del evento GastoRegistrado (publicado por modules/gastos).
    El wiring se hace en modules/alertas/apps.py::ready() con
    event_bus.suscribir(GastoRegistrado, caso.manejar).

    Cuando llega un GastoRegistrado que corresponde a un servicio fijo:
      1. si evento.servicio_fijo_id is None -> no hay alerta que resolver,
         return.
      2. alerta = self.repositorio.obtener_por_servicio_y_periodo(
             evento.servicio_fijo_id, evento.periodo_mes, evento.periodo_anio)
      3. si no hay alerta (o ya estaba resuelta) -> return.
      4. alerta.resolver(evento.gasto_id)   (transicion de dominio)
      5. self.repositorio.actualizar(alerta)

    Es un handler: NO propaga excepciones al publicador del evento (un
    pago no debe fallar porque la alerta no se pudo actualizar). Decidi
    como loguear los errores.

    Params de manejar(): evento: GastoRegistrado
    Retorno: None
    """

    repositorio: AlertaPagoRepository

    def manejar(self, evento: GastoRegistrado) -> None:
        if evento.servicio_fijo_id is None:
            return                                   # gasto puntual: no hay alerta
        try:
            alerta = self.repositorio.obtener_por_servicio_y_periodo(
                evento.servicio_fijo_id, evento.periodo_mes, evento.periodo_anio)
            if alerta is None or alerta.esta_resuelta():
                return
            alerta.resolver(evento.gasto_id)
            self.repositorio.actualizar(alerta)
        except Exception:                            # noqa: BLE001
            logger.exception("No se pudo resolver la alerta para el evento %r", evento)
