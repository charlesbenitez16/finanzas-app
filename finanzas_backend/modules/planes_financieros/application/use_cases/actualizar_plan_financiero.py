"""Caso de uso: actualizar un plan financiero existente."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from django.db import transaction

from modules.planes_financieros.domain.entities import PlanFinanciero
from modules.planes_financieros.domain.exceptions import (
    PlanNoEncontrado,
    PorcentajesNoSuman100,
)
from modules.planes_financieros.domain.ports.repositories import (
    PlanFinancieroRepository,
)


@dataclass
class ActualizarPlanFinancieroUseCase:
    """
    CONSIGNA
    --------
    Actualiza un plan financiero EXISTENTE del usuario autenticado
    (nombre, porcentajes, fechas y, opcionalmente, si queda activo).

      1. plan = obtener_por_id(plan_id). Si no existe, o existe pero es
         de OTRO usuario, => PlanNoEncontrado (no se distingue "no existe"
         de "no es tuyo": no le confirmamos a nadie que un id ajeno existe).
      2. Mutar los campos de ESA entidad (no crear una PlanFinanciero
         nueva desde cero): tiene que conservar su `id` real para que el
         UPDATE en infrastructure/repositories.py afecte la fila correcta
         en vez de hacer `WHERE id IS NULL` (0 filas).
      3. Validar porcentajes_suman_100() con los valores ya actualizados.
      4. Si se pide activo=True y HABIA otro plan activo de este mismo
         usuario, desactivarlo primero (misma regla que
         ActivarPlanFinancieroUseCase) para no romper
         uq_plan_activo_usuario (solo un plan activo por usuario).
         Si activo es None (no lo mandaron), el estado activo/inactivo
         del plan queda TAL CUAL estaba -- no se toca.
      5. Persistir con self.repositorio.actualizar(plan).

    fecha_inicio / fecha_fin en None significa "no lo mandaron": se deja
    el valor que el plan ya tenia (no se pisa con None).

    Params de ejecutar(): plan_id, usuario_id, porcentaje_gasto_fijo,
        porcentaje_ahorro, porcentaje_gasto_libre, activo (opcional),
        nombre, fecha_inicio, fecha_fin
    Retorno: PlanFinanciero (ya actualizado)
    """

    repositorio: PlanFinancieroRepository

    def ejecutar(
        self,
        plan_id: int,
        usuario_id: int,
        porcentaje_gasto_fijo: Decimal,
        porcentaje_ahorro: Decimal,
        porcentaje_gasto_libre: Decimal,
        activo: Optional[bool] = None,
        nombre: str = "Mi plan",
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
    ) -> PlanFinanciero:
        plan = self.repositorio.obtener_por_id(plan_id)
        if plan is None or plan.usuario_id != usuario_id:
            raise PlanNoEncontrado(f"No existe el plan {plan_id}")

        plan.nombre = nombre
        plan.porcentaje_gasto_fijo = porcentaje_gasto_fijo
        plan.porcentaje_ahorro = porcentaje_ahorro
        plan.porcentaje_gasto_libre = porcentaje_gasto_libre
        if fecha_inicio is not None:
            plan.fecha_inicio = fecha_inicio
        if fecha_fin is not None:
            plan.fecha_fin = fecha_fin

        if not plan.porcentajes_suman_100():
            raise PorcentajesNoSuman100("Los porcentajes deben sumar 100")

        with transaction.atomic():
            if activo is not None:
                if activo and not plan.activo:
                    activo_actual = self.repositorio.obtener_plan_activo(usuario_id)
                    if activo_actual is not None and activo_actual.id != plan.id:
                        activo_actual.activo = False
                        self.repositorio.actualizar(activo_actual)  # desactivar PRIMERO
                plan.activo = activo
            return self.repositorio.actualizar(plan)  # activar/guardar DESPUES
