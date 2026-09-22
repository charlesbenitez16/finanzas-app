"""
    Implementacion de NotificadorEmail usando el sistema de envio de
    Django (django.core.mail), configurado por EMAIL_BACKEND en
    settings (consola en dev, SMTP real en produccion).
"""

from django.conf import settings
from django.core.mail import send_mail

from modules.alertas.domain.ports.notificaciones import NotificadorEmail


class DjangoEmailNotificador(NotificadorEmail):
    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
            send_mail(
                subject=asunto,
                message=cuerpo,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[destinatario],
                fail_silently=False,
            )