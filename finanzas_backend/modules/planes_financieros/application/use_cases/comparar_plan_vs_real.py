"""Caso de uso: comparar el plan financiero activo contra la ejecucion real de un mes."""

from dataclasses import dataclass

from modules.gastos.application.use_cases.calcular_balance_mensual import (
    CalcularBalanceMensualUseCase,
)
from modules.planes_financieros.domain.entities import ComparativaPlanVsReal
from modules.planes_financieros.domain.exceptions import PlanNoEncontrado
from modules.planes_financieros.domain.ports.repositories import (
    PlanFinancieroRepository,
)


@dataclass
class CompararPlanVsRealUseCase:
    """
    CONSIGNA
    --------
    Reproduce vista_plan_vs_real para el usuario y periodo dados:

      1. plan = self.plan_repositorio.obtener_plan_activo(usuario_id)
         -> None => PlanNoEncontrado (el usuario no tiene plan activo).
      2. balance = self.calcular_balance.ejecutar(usuario_id, mes, anio)
         (reusa CalcularBalanceMensualUseCase del modulo gastos: da
         total_ingresos, total_gastos y balance).
      3. metas = plan.meta_gasto_fijo(total_ingresos),
                 plan.meta_ahorro(total_ingresos),
                 plan.meta_gasto_libre(total_ingresos)
      4. devolver ComparativaPlanVsReal(...) con metas + gasto_real
         (= balance.total_gastos) + balance_real (= balance.balance).

    Este caso de uso compone otro caso de uso (el de balance): es
    aceptable. Se inyecta ya construido para no acoplar este modulo a los
    repos concretos de ingresos/gastos.

    Params de ejecutar(): usuario_id: int, periodo_mes: int, periodo_anio: int
    Retorno: ComparativaPlanVsReal
    """

    plan_repositorio: PlanFinancieroRepository
    calcular_balance: CalcularBalanceMensualUseCase

    def ejecutar(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> ComparativaPlanVsReal:
        plan = self.plan_repositorio.obtener_plan_activo(usuario_id)
        if plan is None:
            raise PlanNoEncontrado("El usuario no tiene un plan activo")
        balance = self.calcular_balance.ejecutar(usuario_id, periodo_mes, periodo_anio)
        ingresos = balance.total_ingresos
        return ComparativaPlanVsReal(
            usuario_id=usuario_id, periodo_mes=periodo_mes, periodo_anio=periodo_anio,
            total_ingresos=ingresos,
            meta_gasto_fijo=plan.meta_gasto_fijo(ingresos),
            meta_ahorro=plan.meta_ahorro(ingresos),
            meta_gasto_libre=plan.meta_gasto_libre(ingresos),
            gasto_real=balance.total_gastos,
            balance_real=balance.balance,
        )
