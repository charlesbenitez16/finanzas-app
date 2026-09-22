"""Caso de uso: balance mensual de un usuario (ingresos - gastos)."""

from dataclasses import dataclass

from modules.gastos.domain.entities import BalanceMensual
from modules.gastos.domain.ports.repositories import GastoRepository
from modules.ingresos.domain.ports.repositories import IngresoRepository


@dataclass
class CalcularBalanceMensualUseCase:
    """
    CONSIGNA
    --------
    Reproduce vista_balance_mensual para UN usuario y UN periodo:

        total_ingresos = SUM(ingresos.monto)  del periodo
        total_gastos   = SUM(gastos.monto)    del periodo
        balance        = total_ingresos - total_gastos

    Este caso de uso CRUZA dos modulos: recibe por inyeccion tanto el
    puerto de ingresos como el de gastos (ambos son interfaces del
    dominio, no implementaciones: el acoplamiento es aceptable). Cada
    repo ya sabe sumar su lado (sumar_montos_por_periodo).

    Params de ejecutar(): usuario_id: int, periodo_mes: int, periodo_anio: int
    Retorno: BalanceMensual
    """

    ingreso_repositorio: IngresoRepository
    gasto_repositorio: GastoRepository

    def ejecutar(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> BalanceMensual:
        total_ing = self.ingreso_repositorio.sumar_montos_por_periodo(
            usuario_id, periodo_mes, periodo_anio)
        total_gas = self.gasto_repositorio.sumar_montos_por_periodo(
            usuario_id, periodo_mes, periodo_anio)
        return BalanceMensual(
            usuario_id=usuario_id, periodo_mes=periodo_mes, periodo_anio=periodo_anio,
            total_ingresos=total_ing, total_gastos=total_gas,
            balance=total_ing - total_gas,
        )
