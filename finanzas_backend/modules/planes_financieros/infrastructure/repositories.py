"""
Implementacion Django ORM de los puertos de planes_financieros. El
metodo _a_entidad() traduce PlanFinancieroModel -> PlanFinanciero.
"""

from typing import Optional

from modules.planes_financieros.domain.entities import PlanFinanciero
from modules.planes_financieros.domain.ports.repositories import (
    PlanFinancieroRepository,
)
from modules.planes_financieros.infrastructure.models import PlanFinancieroModel
from typing import Optional

class DjangoPlanFinancieroRepository(PlanFinancieroRepository):
    def _a_entidad(self, m: PlanFinancieroModel) -> PlanFinanciero:
        """
        CONSIGNA: PlanFinancieroModel -> PlanFinanciero. Usa
        modelo.usuario_id (id plano), no modelo.usuario.

        Retorno: PlanFinanciero
        """
        return PlanFinanciero(
            id=m.id, usuario_id=m.usuario_id, nombre=m.nombre,
            porcentaje_gasto_fijo=m.porcentaje_gasto_fijo,
            porcentaje_ahorro=m.porcentaje_ahorro,
            porcentaje_gasto_libre=m.porcentaje_gasto_libre,
            fecha_inicio=m.fecha_inicio, fecha_fin=m.fecha_fin, activo=m.activo,
        )

    def obtener_por_id(self, plan_id: int) -> Optional[PlanFinanciero]:
        try:
            return self._a_entidad(PlanFinancieroModel.objects.get(id=plan_id))
        except PlanFinancieroModel.DoesNotExist:
            return None

    def crear(self, plan: PlanFinanciero) -> PlanFinanciero:
        m = PlanFinancieroModel.objects.create(
            usuario_id=plan.usuario_id, nombre=plan.nombre,
            porcentaje_gasto_fijo=plan.porcentaje_gasto_fijo,
            porcentaje_ahorro=plan.porcentaje_ahorro,
            porcentaje_gasto_libre=plan.porcentaje_gasto_libre,
            fecha_inicio=plan.fecha_inicio, fecha_fin=plan.fecha_fin,
            activo=plan.activo,
        )
        return self._a_entidad(m)

    def actualizar(self, plan: PlanFinanciero) -> PlanFinanciero:
        PlanFinancieroModel.objects.filter(id=plan.id).update(
            nombre=plan.nombre, porcentaje_gasto_fijo=plan.porcentaje_gasto_fijo,
            porcentaje_ahorro=plan.porcentaje_ahorro,
            porcentaje_gasto_libre=plan.porcentaje_gasto_libre,
            fecha_inicio=plan.fecha_inicio, fecha_fin=plan.fecha_fin,
            activo=plan.activo,
        )
        return plan

    def listar_por_usuario(self, usuario_id: int) -> list[PlanFinanciero]:
        qs = PlanFinancieroModel.objects.filter(usuario_id=usuario_id).order_by("-fecha_inicio")
        return [self._a_entidad(m) for m in qs]

    def obtener_plan_activo(self, usuario_id: int) -> Optional[PlanFinanciero]:
        m = PlanFinancieroModel.objects.filter(usuario_id=usuario_id, activo=True).first()
        return self._a_entidad(m) if m else None
