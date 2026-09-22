"""Caso de uso: total de ingresos de un usuario en un periodo."""

from dataclasses import dataclass
from decimal import Decimal

from modules.ingresos.domain.ports.repositories import IngresoRepository


@dataclass
class CalcularTotalIngresosPeriodoUseCase:
    """
    CONSIGNA
    --------
    Devuelve la suma de ingresos de un usuario en un periodo. Es la mitad
    "ingresos" de vista_balance_mensual (la otra mitad, gastos, la
    resuelve modules/gastos). CalcularBalanceMensualUseCase (en el modulo
    gastos) compone este resultado con el total de gastos para obtener el
    balance.

    Params de ejecutar(): usuario_id: int, periodo_mes: int, periodo_anio: int
    Retorno: Decimal
    """

    repositorio: IngresoRepository

    def ejecutar(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> Decimal:
        # TODO: [return self.repositorio.sumar_montos_por_periodo(
        #        usuario_id, periodo_mes, periodo_anio).]

        return self.repositorio.sumar_montos_por_periodo(usuario_id,periodo_mes,periodo_anio)
