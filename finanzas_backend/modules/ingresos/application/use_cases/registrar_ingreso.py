"""Caso de uso: registrar un ingreso de un usuario en un periodo."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from modules.ingresos.domain.entities import Ingreso
from modules.ingresos.domain.exceptions import MontoInvalido, PeriodoInvalido
from modules.ingresos.domain.ports.repositories import IngresoRepository


@dataclass
class RegistrarIngresoUseCase:
    """
    CONSIGNA
    --------
    Da de alta un Ingreso. Reglas:
      1. monto > 0                       -> si no, MontoInvalido
      2. 1 <= periodo_mes <= 12          -> si no, PeriodoInvalido
      3. periodo_anio razonable (> 2000) -> si no, PeriodoInvalido
      4. construir Ingreso (sin id) y persistir con el repositorio.

    Params de ejecutar():
        usuario_id: int
        monto: Decimal
        fecha: date
        periodo_mes: int
        periodo_anio: int
        fuente: Optional[str]
        descripcion: Optional[str]
    Retorno: Ingreso (ya con id)
    """

    repositorio: IngresoRepository

    def ejecutar(
        self,
        usuario_id: int,
        monto: Decimal,
        fecha: date,
        periodo_mes: int,
        periodo_anio: int,
        fuente: Optional[str] = None,
        descripcion: Optional[str] = None,
    ) -> Ingreso:

        if monto <= 0:
            raise MontoInvalido("El monto ingresado debe ser mayor a 0")

        if periodo_mes < 1 or periodo_mes > 12:
            raise PeriodoInvalido("Mes invalido")

        if periodo_anio < 2026:
            raise PeriodoInvalido("anio no concuerda con el rango actual")

        ingreso = Ingreso(usuario_id=usuario_id, monto=monto,fecha=fecha,periodo_mes=periodo_mes, periodo_anio=periodo_anio, fuente=(fuente or None), descripcion=(descripcion or None))

        return self.repositorio.crear(ingreso)

