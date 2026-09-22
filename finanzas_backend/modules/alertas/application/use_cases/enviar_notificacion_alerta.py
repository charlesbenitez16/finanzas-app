"""Caso de uso / handler: enviar el email de una alerta recien generada."""

import logging
from dataclasses import dataclass

from django.contrib.auth import get_user_model

from modules.alertas.domain.events import AlertaGenerada
from modules.alertas.domain.ports.notificaciones import NotificadorEmail
from modules.alertas.domain.ports.repositories import AlertaPagoRepository

logger = logging.getLogger(__name__)
AuthUser = get_user_model()


@dataclass
class EnviarNotificacionAlertaUseCase:
        """
        Suscriptor de AlertaGenerada (se registra en alertas/apps.py::ready).
        Busca el email en auth_user (NO en usuarios: usuario_id es el id
        de auth_user en toda la app), arma el mensaje, lo manda por el
        puerto NotificadorEmail y, si salio bien, marca la alerta como
        'Enviada'. Si algo falla (el mail no salio, el usuario no tiene
        email, lo que sea), solo loguea: un email que falla NO debe
        tumbar el resto del job de generar alertas ni el request que lo
        disparo (mismo criterio que ResolverAlertaAlPagarUseCase).
        """

        repositorio: AlertaPagoRepository
        notificador: NotificadorEmail

        def manejar(self, evento: AlertaGenerada) -> None:
            try:
                alerta = self.repositorio.obtener_por_id(evento.alerta_id)
                if alerta is None or not alerta.esta_pendiente():
                    return
                auth_user = AuthUser.objects.filter(id=evento.usuario_id).first()
                if auth_user is None or not auth_user.email:
                    logger.warning(
                        "Usuario %s sin email valido, no se envia la alerta %s",
                        evento.usuario_id, evento.alerta_id,
                    )
                    return
                self.notificador.enviar(
                    destinatario=auth_user.email,
                    asunto="Recordatorio de pago - Finanzas",
                    cuerpo=evento.mensaje,
                )
                alerta.marcar_enviada()
                self.repositorio.actualizar(alerta)
            except Exception:
                logger.exception(
                    "No se pudo enviar el email de la alerta %s", evento.alerta_id
                )