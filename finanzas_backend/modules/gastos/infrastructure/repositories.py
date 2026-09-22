"""
Implementacion Django ORM de los puertos de gastos. Ademas del mapeo
_a_entidad(), aca viven las traducciones de las vistas SQL A, B y C a
consultas del ORM.
"""

from decimal import Decimal
from typing import Optional
from django.db.models import Sum

from modules.gastos.domain.entities import AhorroPorPrioridad, Gasto
from modules.gastos.domain.ports.repositories import GastoRepository
from modules.gastos.infrastructure.models import GastoModel


class DjangoGastoRepository(GastoRepository):
    def _a_entidad(self, m: GastoModel) -> Gasto:
        """
        CONSIGNA: GastoModel -> Gasto. Usa los ids planos
        (modelo.usuario_id, modelo.categoria_id, modelo.servicio_fijo_id,
        modelo.prioridad_id), no las relaciones completas.

        Retorno: Gasto
        """
        return Gasto(
                id=m.id, usuario_id=m.usuario_id, categoria_id=m.categoria_id,
                servicio_fijo_id=m.servicio_fijo_id, prioridad_id=m.prioridad_id,
                monto=m.monto, fecha_gasto=m.fecha_gasto, periodo_mes=m.periodo_mes,
                periodo_anio=m.periodo_anio, estado=m.estado,
                descripcion=m.descripcion, fecha_registro=m.fecha_registro,
            )

    def obtener_por_id(self, gasto_id: int) -> Optional[Gasto]:
            try:
                return self._a_entidad(GastoModel.objects.get(id=gasto_id))
            except GastoModel.DoesNotExist:
                return None

    def crear(self, gasto: Gasto) -> Gasto:
            m = GastoModel.objects.create(
                usuario_id=gasto.usuario_id, categoria_id=gasto.categoria_id,
                servicio_fijo_id=gasto.servicio_fijo_id,
                prioridad_id=gasto.prioridad_id, monto=gasto.monto,
                fecha_gasto=gasto.fecha_gasto, periodo_mes=gasto.periodo_mes,
                periodo_anio=gasto.periodo_anio, estado=gasto.estado,
                descripcion=gasto.descripcion,
            )
            return self._a_entidad(m)

    def listar_por_usuario_y_periodo(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> list[Gasto]:
            qs = GastoModel.objects.filter(
                usuario_id=usuario_id, periodo_mes=periodo_mes,
                periodo_anio=periodo_anio,
            ).order_by("fecha_gasto")
            return [self._a_entidad(m) for m in qs]

    def sumar_montos_por_periodo(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> Decimal:
            total = GastoModel.objects.filter(
                usuario_id=usuario_id, periodo_mes=periodo_mes,
                periodo_anio=periodo_anio,
            ).aggregate(t=Sum("monto"))["t"]
            return total or Decimal("0")

    def existe_pago_de_servicio_en_periodo(
        self, servicio_fijo_id: int, periodo_mes: int, periodo_anio: int
    ) -> bool:
            return GastoModel.objects.filter(
                servicio_fijo_id=servicio_fijo_id, periodo_mes=periodo_mes,
                periodo_anio=periodo_anio,
            ).exists()

    def listar_pagos_de_servicio_fijo(self, servicio_fijo_id: int) -> list[Gasto]:
            qs = GastoModel.objects.filter(
                servicio_fijo_id=servicio_fijo_id,
            ).order_by("periodo_anio", "periodo_mes")
            return [self._a_entidad(m) for m in qs]

    def total_por_prioridad(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> list[AhorroPorPrioridad]:
            filas = (
                GastoModel.objects
                .filter(usuario_id=usuario_id, periodo_mes=periodo_mes,
                        periodo_anio=periodo_anio)
                .values("prioridad__nombre", "prioridad__nivel_orden")
                .annotate(total=Sum("monto"))
                .order_by("prioridad__nivel_orden")
            )
            return [
                AhorroPorPrioridad(
                    prioridad=f["prioridad__nombre"],
                    nivel_orden=f["prioridad__nivel_orden"],
                    total_por_prioridad=f["total"],
                )
                for f in filas
            ]
