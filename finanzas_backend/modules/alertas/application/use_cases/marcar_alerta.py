"""
Casos de uso de transicion de estado de una alerta:
Pendiente -> Enviada -> Leida.

Van juntos en un archivo porque comparten estructura (buscar la alerta,
aplicar la transicion de dominio, persistir). Si preferis un archivo por
caso de uso -- como el resto del proyecto -- separalos.
"""

from dataclasses import dataclass

from modules.alertas.domain.entities import AlertaPago
from modules.alertas.domain.exceptions import AlertaNoEncontrada
from modules.alertas.domain.ports.repositories import AlertaPagoRepository


@dataclass
class MarcarAlertaComoEnviadaUseCase:
    """
    CONSIGNA: aplicar la transicion Pendiente -> Enviada.
      1. alerta = obtener_por_id(alerta_id) -> None => AlertaNoEncontrada
      2. alerta.marcar_enviada()  (puede lanzar TransicionEstadoInvalida)
      3. return self.repositorio.actualizar(alerta)

    Params de ejecutar(): alerta_id: int
    Retorno: AlertaPago
    """

    repositorio: AlertaPagoRepository

    def ejecutar(self, alerta_id: int) -> AlertaPago:
        alerta = self.repositorio.obtener_por_id(alerta_id)
        if alerta is None:
            raise AlertaNoEncontrada(f"No existe la alerta {alerta_id}")
        alerta.marcar_enviada()              # puede lanzar TransicionEstadoInvalida
        return self.repositorio.actualizar(alerta)


@dataclass
class MarcarAlertaComoLeidaUseCase:
    """
    CONSIGNA: idem la anterior pero con la transicion Enviada -> Leida
    (alerta.marcar_leida()).

    Params de ejecutar(): alerta_id: int
    Retorno: AlertaPago
    """

    repositorio: AlertaPagoRepository

    def ejecutar(self, alerta_id: int) -> AlertaPago:
        alerta = self.repositorio.obtener_por_id(alerta_id)
        if alerta is None:
            raise AlertaNoEncontrada(f"No existe la alerta {alerta_id}")
        alerta.marcar_leida()              # puede lanzar TransicionEstadoInvalida
        return self.repositorio.actualizar(alerta)
