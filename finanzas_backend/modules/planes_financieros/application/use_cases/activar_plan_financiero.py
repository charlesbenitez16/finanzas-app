"""Caso de uso: activar un plan financiero (y desactivar el anterior)."""

from dataclasses import dataclass

from modules.planes_financieros.domain.entities import PlanFinanciero
from modules.planes_financieros.domain.exceptions import PlanNoEncontrado
from modules.planes_financieros.domain.ports.repositories import (
    PlanFinancieroRepository,
)

from django.db import transaction

@dataclass
class ActivarPlanFinancieroUseCase:
    """
    CONSIGNA
    --------
    Hace de `plan_id` el plan activo del usuario, respetando
    uq_plan_activo_usuario (solo un plan activo por usuario a la vez):

      1. plan = obtener_por_id(plan_id) -> None => PlanNoEncontrado
      2. activo_actual = obtener_plan_activo(plan.usuario_id)
      3. si hay activo_actual y no es el mismo: desactivarlo y persistir
      4. marcar `plan` como activo y persistir

    Pensa el orden de las escrituras: si el indice unico es estricto,
    tenes que desactivar el viejo ANTES de activar el nuevo (o hacerlo en
    una transaccion). Deja un TODO con la estrategia elegida.

    Params de ejecutar(): plan_id: int
    Retorno: PlanFinanciero (el que quedo activo)
    """

    repositorio: PlanFinancieroRepository

    def ejecutar(self, plan_id: int) -> PlanFinanciero:
        plan = self.repositorio.obtener_por_id(plan_id)
        if plan is None:
            raise PlanNoEncontrado(f"No existe el plan {plan_id}")
        with transaction.atomic():
            activo = self.repositorio.obtener_plan_activo(plan.usuario_id)
            if activo is not None and activo.id != plan.id:
                activo.activo = False
                self.repositorio.actualizar(activo)     # DESACTIVAR primero
            plan.activo = True
            return self.repositorio.actualizar(plan)    # ACTIVAR después
