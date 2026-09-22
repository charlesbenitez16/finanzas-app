"""
Entidad de dominio del modulo ingresos: Ingreso.

Python puro (dataclass), sin Django. Mapea la tabla `ingresos` de
schema_finanzas.sql: montos variables mes a mes, agrupados por periodo
(mes/anio).
"""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from shared.domain.base_entity import Entity


@dataclass
class Ingreso(Entity):
    """
    Un ingreso puntual de un usuario en un periodo (ej. "Salario enero",
    "Freelance marzo").

    CONSIGNA
    --------
    Aca solo vive comportamiento que el Ingreso resuelve con sus PROPIOS
    atributos. El agregado por periodo (sumar todos los ingresos de un
    mes) NO es de la entidad: necesita ver a los demas ingresos, asi que
    vive en el repositorio / caso de uso (mismo criterio que el metodo
    es_prescindible() que se elimino en catalogos).

    Campos (ver 01_schema.sql tabla `ingresos`):
        usuario_id   -- FK a usuarios (NOT NULL)
        monto        -- NUMERIC(12,2), CHECK (monto > 0)
        fecha        -- fecha real del ingreso
        periodo_mes  -- SMALLINT 1..12
        periodo_anio -- SMALLINT
        fuente       -- 'Salario', 'Freelance', 'Bono', 'Renta', ...
        descripcion  -- texto libre

    Nota: shared/domain/value_objects.py tiene un value object `Periodo`
    (mes/anio) que podrias usar aca en vez de dos ints sueltos. Esta
    como kata a medio hacer; queda a tu criterio adoptarlo.
    """

    usuario_id: Optional[int] = None
    monto: Decimal = Decimal("0")
    fecha: Optional[date] = None
    periodo_mes: int = 0
    periodo_anio: int = 0
    fuente: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_registro: Optional[datetime] = None

    def pertenece_al_periodo(self, mes: int, anio: int) -> bool:
        """
        CONSIGNA: True si este ingreso cae en el periodo (mes, anio) dado.

        Params: mes (1..12), anio (int)
        Retorno: bool
        """
        # TODO: [comparacion directa de self.periodo_mes / self.periodo_anio.]
        if self.periodo_mes == mes and self.periodo_anio == anio:
            return True
        return False
        #raise NotImplementedError("Implementar este metodo")

    def es_monto_valido(self) -> bool:
        """
        CONSIGNA: replica el CHECK (monto > 0) del schema como invariante
        de dominio.

        Retorno: bool
        """
        # TODO: [self.monto > 0. Pensa si en vez de un metodo consultable
        #        conviene validar en __post_init__ y lanzar ValueError.]

        if self.monto > 0:
            return True
        
        raise ValueError("No es monto valido")
