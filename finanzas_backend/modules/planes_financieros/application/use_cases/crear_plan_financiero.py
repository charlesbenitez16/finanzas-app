"""Caso de uso: crear un plan financiero para un usuario."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from modules.planes_financieros.domain.entities import PlanFinanciero
from modules.planes_financieros.domain.exceptions import PorcentajesNoSuman100
from modules.planes_financieros.domain.ports.repositories import (
    PlanFinancieroRepository,
)


@dataclass
class CrearPlanFinancieroUseCase:
    """
    CONSIGNA
    --------
    Crea un PlanFinanciero. Reglas:
      1. porcentaje_gasto_fijo + porcentaje_ahorro + porcentaje_gasto_libre
         == 100  -> si no, PorcentajesNoSuman100. Usa
         PlanFinanciero.porcentajes_suman_100() (la entidad valida su
         propia invariante).
      2. Decidi si un plan recien creado nace activo o inactivo. Si nace
         activo y el usuario ya tiene uno, tenes el conflicto de
         uq_plan_activo_usuario: o lo creas inactivo y obligas a llamar a
         ActivarPlanFinancieroUseCase, o encadenas la desactivacion aca.
         Deja tu decision como TODO.

    Params de ejecutar(): usuario_id, nombre, porcentaje_gasto_fijo,
        porcentaje_ahorro, porcentaje_gasto_libre, fecha_inicio, fecha_fin
    Retorno: PlanFinanciero (con id)
    """

    repositorio: PlanFinancieroRepository

    def ejecutar(
        self,
        usuario_id: int,
        porcentaje_gasto_fijo: Decimal,
        porcentaje_ahorro: Decimal,
        porcentaje_gasto_libre: Decimal,
        nombre: str = "Mi plan",
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
    ) -> PlanFinanciero:
        plan = PlanFinanciero(
            usuario_id=usuario_id, nombre=nombre,
            porcentaje_gasto_fijo=porcentaje_gasto_fijo,
            porcentaje_ahorro=porcentaje_ahorro,
            porcentaje_gasto_libre=porcentaje_gasto_libre,
            fecha_inicio=fecha_inicio or date.today(), fecha_fin=fecha_fin,
            activo=False,                    # nace INACTIVO
        )
        if not plan.porcentajes_suman_100():
            raise PorcentajesNoSuman100("Los porcentajes deben sumar 100")
        return self.repositorio.crear(plan)
