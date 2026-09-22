"""
Implementacion Django ORM de los puertos de servicios_fijos. El metodo
_a_entidad() traduce ServicioFijoModel -> ServicioFijo.
"""

from datetime import date
from typing import Optional

from modules.servicios_fijos.domain.entities import ServicioFijo
from modules.servicios_fijos.domain.ports.repositories import ServicioFijoRepository
from modules.servicios_fijos.infrastructure.models import ServicioFijoModel


class DjangoServicioFijoRepository(ServicioFijoRepository):
    def _a_entidad(self, modelo: ServicioFijoModel) -> ServicioFijo:
        """
        CONSIGNA: ServicioFijoModel -> ServicioFijo. Usa modelo.categoria_id
        / modelo.prioridad_id / modelo.usuario_id (los ids planos), no las
        relaciones completas, para no disparar consultas extra.

        Retorno: ServicioFijo
        """
        return ServicioFijo(
            id=modelo.id,
            usuario_id=modelo.usuario_id,
            categoria_id=modelo.categoria_id,
            prioridad_id= modelo.prioridad_id,
            nombre=modelo.nombre,
            dia_vencimiento=modelo.dia_vencimiento,
            monto_estimado=modelo.monto_estimado,
            es_monto_variable=modelo.es_monto_variable,
            dias_anticipacion_alerta=modelo.dias_anticipacion_alerta,
            activo=modelo.activo,
            fecha_inicio=modelo.fecha_inicio,
            fecha_fin=modelo.fecha_fin,
            notas=modelo.notas
        )

    def obtener_por_id(self, servicio_id: int) -> Optional[ServicioFijo]:

        try:
            return self._a_entidad(ServicioFijoModel.objects.get(id=servicio_id))
        except ServicioFijoModel.DoesNotExist:
            return None

    def crear(self, servicio: ServicioFijo) -> ServicioFijo:
       
        modelo = ServicioFijoModel.objects.create(
            #id=modelo.id,
            usuario_id=servicio.usuario_id,
            categoria_id=servicio.categoria_id,
            prioridad_id= servicio.prioridad_id,
            nombre=servicio.nombre,
            dia_vencimiento=servicio.dia_vencimiento,
            monto_estimado=servicio.monto_estimado,
            es_monto_variable=servicio.es_monto_variable,
            dias_anticipacion_alerta=servicio.dias_anticipacion_alerta,
            activo=servicio.activo,
            fecha_inicio=servicio.fecha_inicio,
            fecha_fin=servicio.fecha_fin,
            notas=servicio.notas
        )

        return self._a_entidad(modelo)

    def actualizar(self, servicio: ServicioFijo) -> ServicioFijo:
        # TODO: [get por servicio.id, actualizar campos, save(); devolver
        #        la entidad recargada.]
        ServicioFijoModel.objects.filter(id=servicio.id).update(
            nombre=servicio.nombre, 
            dia_vencimiento=servicio.dia_vencimiento,
            monto_estimado=servicio.monto_estimado,
            es_monto_variable=servicio.es_monto_variable,
            dias_anticipacion_alerta=servicio.dias_anticipacion_alerta,
            activo=servicio.activo, 
            fecha_inicio=servicio.fecha_inicio,
            fecha_fin=servicio.fecha_fin, 
            notas=servicio.notas,
        )

        return servicio

    def listar_por_usuario(
        self, usuario_id: int, solo_activos: bool = False
    ) -> list[ServicioFijo]:
        # TODO: [queryset = ServicioFijoModel.objects.filter(usuario_id=usuario_id);
        #        if solo_activos: queryset = queryset.filter(activo=True);
        #        queryset.order_by("nombre"); mapear con _a_entidad.]
        
        modelo = ServicioFijoModel.objects.filter(usuario_id=usuario_id)

        if solo_activos:
            modelo = modelo.filter(activo=True).order_by("nombre")

        
        return [self._a_entidad(o) for o in modelo]

    def listar_proximos_a_vencer(
        self, fecha_referencia: date
    ) -> list[ServicioFijo]:

        activos = [self._a_entidad(m) for m in ServicioFijoModel.objects.filter(activo=True)]

        return [s for s in activos if s.debe_generar_alerta(fecha_referencia)]
