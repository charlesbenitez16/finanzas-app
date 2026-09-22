"""
Implementacion Django ORM de los puertos de alertas. El metodo
_a_entidad() traduce AlertaPagoModel -> AlertaPago.
"""

from typing import Optional

from modules.alertas.domain.entities import AlertaPago
from modules.alertas.domain.ports.repositories import AlertaPagoRepository
from modules.alertas.infrastructure.models import AlertaPagoModel


class DjangoAlertaPagoRepository(AlertaPagoRepository):
    def _a_entidad(self, m: AlertaPagoModel) -> AlertaPago:
        """
        CONSIGNA: AlertaPagoModel -> AlertaPago. Usa los ids planos
        (modelo.usuario_id, modelo.servicio_fijo_id, modelo.gasto_id).

        Retorno: AlertaPago
        """
        return AlertaPago(
            id=m.id, usuario_id=m.usuario_id, servicio_fijo_id=m.servicio_fijo_id,
            gasto_id=m.gasto_id, periodo_mes=m.periodo_mes, periodo_anio=m.periodo_anio,
            fecha_alerta=m.fecha_alerta, estado=m.estado, mensaje=m.mensaje,
            fecha_creacion=m.fecha_creacion,
        )

    def obtener_por_id(self, alerta_id: int) -> Optional[AlertaPago]:
        try:
            return self._a_entidad(AlertaPagoModel.objects.get(id=alerta_id))
        except AlertaPagoModel.DoesNotExist:
            return None

    def crear(self, alerta: AlertaPago) -> AlertaPago:
        m = AlertaPagoModel.objects.create(
            usuario_id=alerta.usuario_id, servicio_fijo_id=alerta.servicio_fijo_id,
            gasto_id=alerta.gasto_id, periodo_mes=alerta.periodo_mes,
            periodo_anio=alerta.periodo_anio, fecha_alerta=alerta.fecha_alerta,
            estado=alerta.estado, mensaje=alerta.mensaje,
        )
        return self._a_entidad(m)

    def actualizar(self, alerta: AlertaPago) -> AlertaPago:
        AlertaPagoModel.objects.filter(id=alerta.id).update(
            gasto_id=alerta.gasto_id, estado=alerta.estado, mensaje=alerta.mensaje,
        )
        return alerta

    def listar_por_usuario_y_estado(
        self, usuario_id: int, estado: str
    ) -> list[AlertaPago]:
        qs = AlertaPagoModel.objects.filter(
            usuario_id=usuario_id, estado=estado,
        ).order_by("fecha_alerta")
        return [self._a_entidad(m) for m in qs]

    def existe_alerta_para_servicio_en_periodo(
        self, servicio_fijo_id: int, periodo_mes: int, periodo_anio: int
    ) -> bool:
        return AlertaPagoModel.objects.filter(
            servicio_fijo_id=servicio_fijo_id, periodo_mes=periodo_mes,
            periodo_anio=periodo_anio,
        ).exists()

    def obtener_por_servicio_y_periodo(
        self, servicio_fijo_id: int, periodo_mes: int, periodo_anio: int
    ) -> Optional[AlertaPago]:
        m = AlertaPagoModel.objects.filter(
            servicio_fijo_id=servicio_fijo_id, periodo_mes=periodo_mes,
            periodo_anio=periodo_anio,
        ).first()
        return self._a_entidad(m) if m else None
