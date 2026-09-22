"""
    Puerto para notificar al usuario por un canal externo a la API. Hoy
    solo email, pero la interfaz queda abierta a otros canales (push,
    SMS) sin que el dominio sepa cual se usa en cada caso.
"""

from abc import ABC, abstractmethod


class NotificadorEmail(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
            """
            Envia un email. Si el envio falla, DEBE dejar propagar la
            excepcion (no la traga acá): la politica de "loguear y
            seguir" vive en el caso de uso que orquesta (mismo criterio
            que ya usa ResolverAlertaAlPagarUseCase), no en el adapter.
            """
            ...
