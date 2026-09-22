"""Eventos de dominio que publica el modulo alertas."""

from dataclasses import dataclass

from shared.domain.events import DomainEvent


@dataclass(frozen=True)
class AlertaGenerada(DomainEvent):
        """
        Se publica cuando GenerarAlertasDeVencimientoUseCase crea una
        alerta nueva. El propio modulo alertas se suscribe (ver
        apps.py::ready) para disparar el email -- separa "generar la
        alerta" de "avisar por mail", mismo patron que GastoRegistrado /
        ResolverAlertaAlPagarUseCase ya usan en este proyecto.
        """

        alerta_id: int = 0
        usuario_id: int = 0
        servicio_fijo_id: int = 0
        mensaje: str = ""