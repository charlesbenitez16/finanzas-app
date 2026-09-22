from django.apps import AppConfig


class AlertasConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.alertas"
    label = "alertas"
    verbose_name = "Alertas de pago"

    def ready(self) -> None:
        """
        CONSIGNA
        --------
        Aca es donde `alertas` se engancha al bus de eventos para
        reaccionar a GastoRegistrado (publicado por modules/gastos).

        Sugerencia de implementacion:
            from shared.domain.events import event_bus
            from modules.gastos.domain.events import GastoRegistrado
            from modules.alertas.application.use_cases.resolver_alerta_al_pagar import (
                ResolverAlertaAlPagarUseCase,
            )
            from modules.alertas.infrastructure.repositories import (
                DjangoAlertaPagoRepository,
            )

            caso = ResolverAlertaAlPagarUseCase(DjangoAlertaPagoRepository())
            event_bus.suscribir(GastoRegistrado, caso.manejar)

        Ojo: ready() corre una sola vez al arrancar. Import diferido (aca
        adentro) para no romper el arranque por imports circulares.
        """
        from shared.domain.events import event_bus
        from modules.gastos.domain.events import GastoRegistrado
        from modules.alertas.domain.events import AlertaGenerada
        from modules.alertas.application.use_cases.resolver_alerta_al_pagar import (
            ResolverAlertaAlPagarUseCase,
        )
        from modules.alertas.application.use_cases.enviar_notificacion_alerta import (
            EnviarNotificacionAlertaUseCase,
        )
        from modules.alertas.infrastructure.repositories import DjangoAlertaPagoRepository
        from modules.alertas.infrastructure.notificaciones import DjangoEmailNotificador

        repo = DjangoAlertaPagoRepository()

        caso_resolver = ResolverAlertaAlPagarUseCase(repositorio=repo)
        event_bus.suscribir(GastoRegistrado, caso_resolver.manejar)

        caso_notificar = EnviarNotificacionAlertaUseCase(
            repositorio=repo, notificador=DjangoEmailNotificador(),
        )
        event_bus.suscribir(AlertaGenerada, caso_notificar.manejar)