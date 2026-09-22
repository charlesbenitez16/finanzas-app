"""Caso de uso: variacion mes a mes del monto de un servicio fijo."""

from dataclasses import dataclass

from modules.gastos.domain.entities import VariacionServicio
from modules.gastos.domain.ports.repositories import GastoRepository
from modules.servicios_fijos.domain.ports.repositories import ServicioFijoRepository
from decimal import Decimal

@dataclass
class CalcularVariacionServiciosUseCase:
    """
    CONSIGNA
    --------
    Reproduce vista_variacion_servicios en Python. Para un servicio fijo,
    traer todos sus pagos ORDENADOS por (periodo_anio, periodo_mes) y, en
    cada uno, calcular:

        porcentaje_variacion = (monto_actual - monto_anterior)
                               / monto_anterior * 100

    donde `monto_anterior` es el del pago inmediatamente previo (el LAG de
    la vista SQL). El primer pago no tiene anterior: monto_anterior y
    porcentaje_variacion quedan en None.

    Podes apoyarte en shared/domain/value_objects.py::Dinero
    (porcentaje_de_variacion_respecto_a) -- tambien esta como kata.

    Params de ejecutar(): servicio_fijo_id: int
    Retorno: list[VariacionServicio] (una por periodo, en orden cronologico)
    """

    repositorio: GastoRepository
    servicio_fijo_repositorio:ServicioFijoRepository

    def ejecutar(self, servicio_fijo_id: int) -> list[VariacionServicio]:
        pagos = self.repositorio.listar_pagos_de_servicio_fijo(servicio_fijo_id)
        resultado = []
        anterior = None
        servicio_obj = self.servicio_fijo_repositorio.obtener_por_id(servicio_fijo_id)
        nombre_servicio = servicio_obj.nombre if servicio_obj else ""
        for pago in pagos:                      # ya vienen ordenados por (anio, mes)
            if anterior is None or anterior.monto == 0:
                pct = None
            else:
                pct = ((pago.monto - anterior.monto) / anterior.monto
                       * Decimal("100")).quantize(Decimal("0.01"))
            resultado.append(VariacionServicio(
                servicio_fijo_id=servicio_fijo_id,
                servicio=nombre_servicio,                    # ver nota
                periodo_mes=pago.periodo_mes, periodo_anio=pago.periodo_anio,
                monto_actual=pago.monto,
                monto_anterior=(anterior.monto if anterior else None),
                porcentaje_variacion=pct,
            ))
            anterior = pago
        return resultado
