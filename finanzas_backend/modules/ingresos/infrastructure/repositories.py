"""
Implementacion Django ORM de los puertos de ingresos. El metodo
_a_entidad() traduce IngresoModel -> Ingreso (ver el mismo patron en
modules/catalogos/infrastructure/repositories.py).
"""

from decimal import Decimal
from typing import Optional
from django.db.models import Sum


from modules.ingresos.domain.entities import Ingreso
from modules.ingresos.domain.ports.repositories import IngresoRepository
from modules.ingresos.infrastructure.models import IngresoModel


class DjangoIngresoRepository(IngresoRepository):
    def _a_entidad(self, modelo: IngresoModel) -> Ingreso:
        """
        CONSIGNA: IngresoModel -> Ingreso. Usa modelo.usuario_id (no
        modelo.usuario) para no disparar una consulta extra por el User.

        Retorno: Ingreso
        """

        return Ingreso(id=modelo.id, usuario_id=modelo.usuario_id, monto=modelo.monto,
                        periodo_mes=modelo.periodo_mes, periodo_anio=modelo.periodo_anio,
                        fuente=modelo.fuente, descripcion=modelo.descripcion,
                        fecha_registro=modelo.fecha_registro,fecha=modelo.fecha)
        

    def obtener_por_id(self, ingreso_id: int) -> Optional[Ingreso]:
        try:
            return self._a_entidad(IngresoModel.objects.get(id=ingreso_id))
        except IngresoModel.DoesNotExist:
            return None

    def crear(self, ingreso: Ingreso) -> Ingreso:
        
        modelo = IngresoModel.objects.create(usuario_id=ingreso.usuario_id, monto=ingreso.monto, 
                    periodo_mes=ingreso.periodo_mes, periodo_anio=ingreso.periodo_anio,
                    fuente=ingreso.fuente, descripcion=ingreso.descripcion, fecha_registro=ingreso.fecha_registro,fecha=ingreso.fecha)

        return self._a_entidad(modelo)

    def listar_por_usuario_y_periodo(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> list[Ingreso]:

        lista_objetos = IngresoModel.objects.filter(usuario_id=usuario_id,periodo_mes=periodo_mes,periodo_anio=periodo_anio).order_by("fecha")
        
        return [self._a_entidad(o) for o in lista_objetos]

    def sumar_montos_por_periodo(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> Decimal:
        # TODO: [.filter(...).aggregate(total=Sum("monto"))["total"] or
        #        Decimal("0"). Equivale al SELECT SUM(monto) del puerto
        #        (lado ingresos de vista_balance_mensual).]
        
        total = IngresoModel.objects.filter(
                usuario_id=usuario_id, periodo_mes=periodo_mes,
                periodo_anio=periodo_anio,
            ).aggregate(total=Sum("monto"))["total"]

        return total or Decimal("0")
        #################################### asi lo hice yo #############################################3
        """lista = self.listar_por_usuario_y_periodo(usuario_id,periodo_mes,periodo_anio)
        suma = 0
        for objeto in lista:
            suma = suma + objeto.monto

        return suma"""


