"""Caso de uso: dar de alta un servicio fijo / gasto recurrente."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from modules.servicios_fijos.domain.entities import ServicioFijo
from modules.servicios_fijos.domain.exceptions import (
    DiaVencimientoInvalido,
    MontoEstimadoInvalido,
    RangoFechasInvalido,
)
from modules.servicios_fijos.domain.ports.repositories import ServicioFijoRepository


@dataclass
class CrearServicioFijoUseCase:
    """
    CONSIGNA
    --------
    Alta de un ServicioFijo. Reglas (todas del CHECK/estructura de
    01_schema.sql):
      1. 1 <= dia_vencimiento <= 31            -> si no, DiaVencimientoInvalido
      2. monto_estimado is None o >= 0         -> si no, MontoEstimadoInvalido
      3. fecha_fin is None o fecha_fin >= fecha_inicio -> si no, RangoFechasInvalido
      4. construir la entidad (sin id, activo=True) y persistir.

    Nota: categoria_id y prioridad_id se reciben como ints. Validar que
    existan es responsabilidad discutible: podes chequearlo aca contra
    los repos de `catalogos`, o confiar en la FK de la base. Deja un TODO
    con tu decision.

    Params de ejecutar(): usuario_id, categoria_id, prioridad_id, nombre,
        dia_vencimiento, monto_estimado, es_monto_variable,
        dias_anticipacion_alerta, fecha_inicio, fecha_fin, notas
    Retorno: ServicioFijo (con id)
    """

    repositorio: ServicioFijoRepository

    def ejecutar(
        self,
        usuario_id: int,
        categoria_id: int,
        prioridad_id: int,
        nombre: str,
        dia_vencimiento: int,
        monto_estimado: Optional[Decimal] = None,
        es_monto_variable: bool = False,
        dias_anticipacion_alerta: int = 3,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        notas: Optional[str] = None,
    ) -> ServicioFijo:


        if fecha_inicio is None:
            fecha_inicio = date.today()

        if dia_vencimiento < 1 or dia_vencimiento > 31:
            raise DiaVencimientoInvalido("Rango de dia invalido")

        if monto_estimado is not None and monto_estimado < 0:
            raise MontoEstimadoInvalido("monto_estimado no puede ser negativo")

        if fecha_fin is not None and fecha_fin < fecha_inicio:
            raise RangoFechasInvalido("fecha_fin es anterior a fecha_inicio")

        servicio_fijo = ServicioFijo(
            usuario_id=usuario_id,
            categoria_id=categoria_id,
            prioridad_id= prioridad_id,
            nombre=nombre,
            dia_vencimiento=dia_vencimiento,
            monto_estimado=monto_estimado,
            es_monto_variable=es_monto_variable,
            dias_anticipacion_alerta=dias_anticipacion_alerta,
            activo=True,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            notas=notas
        )

        return self.repositorio.crear(servicio_fijo)
