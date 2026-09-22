"""
Bus de eventos de dominio en memoria: permite que un modulo publique un
evento sin conocer quien lo escucha, para que otros modulos reaccionen
sin acoplarse directamente entre si (ej. gastos publica GastoRegistrado,
alertas se suscribe para marcar la alerta correspondiente como resuelta).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable


@dataclass(frozen=True)
class DomainEvent:
    """Clase base para eventos de dominio."""

    ocurrido_en: datetime = field(default_factory=datetime.utcnow)


class EventBus:
    def __init__(self) -> None:
        self._suscriptores: dict[type, list[Callable[[DomainEvent], None]]] = {}

    def suscribir(self, tipo_evento: type, manejador: Callable[[DomainEvent], None]) -> None:
        self._suscriptores.setdefault(tipo_evento, []).append(manejador)

    def publicar(self, evento: DomainEvent) -> None:
        for manejador in self._suscriptores.get(type(evento), []):
            manejador(evento)


event_bus = EventBus()
