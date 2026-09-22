"""
Entidad de dominio del modulo servicios_fijos: ServicioFijo.

Python puro (dataclass), sin Django. Mapea la tabla `servicios_fijos` de
schema_finanzas.sql: es la "plantilla" de un gasto recurrente (Internet,
Agua, Luz, Gimnasio...). Cada mes, un ServicioFijo genera un pago real
que se registra como un Gasto en el modulo `gastos`.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from shared.domain.base_entity import Entity

from calendar import monthrange

@dataclass
class ServicioFijo(Entity):
    """
    CONSIGNA
    --------
    Modela un servicio fijo / gasto recurrente. Los metodos de abajo son
    los que la entidad PUEDE resolver mirando solo sus atributos (mas una
    fecha de referencia que se le pasa como parametro). Comparar contra
    los pagos ya registrados (para saber si este mes ya se pago) NO es de
    la entidad: eso necesita el repositorio de gastos y vive en un caso
    de uso.

    Campos (ver 01_schema.sql tabla `servicios_fijos`):
        usuario_id               -- FK usuarios (NOT NULL)
        categoria_id             -- FK categorias_gasto (NOT NULL)
        prioridad_id             -- FK niveles_prioridad (NOT NULL)
        nombre                   -- "Internet Movistar", "Agua"
        dia_vencimiento          -- SMALLINT 1..31
        monto_estimado           -- NUMERIC(12,2) >= 0 (puede ser None)
        es_monto_variable        -- True para agua/luz (cambia cada mes)
        dias_anticipacion_alerta -- cuantos dias antes avisar (default 3)
        activo                   -- baja logica
        fecha_inicio             -- desde cuando aplica
        fecha_fin                -- hasta cuando (None = sin fin)
        notas                    -- texto libre
    """

    usuario_id: Optional[int] = None
    categoria_id: Optional[int] = None
    prioridad_id: Optional[int] = None
    nombre: str = ""
    dia_vencimiento: int = 1
    monto_estimado: Optional[Decimal] = None
    es_monto_variable: bool = False
    dias_anticipacion_alerta: int = 3
    activo: bool = True
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    notas: Optional[str] = None

    def esta_activo(self) -> bool:
        """CONSIGNA: lectura directa del flag `activo`. Retorno: bool."""
        # TODO: [una linea.]
        return self.activo

    def esta_vigente(self, fecha: date) -> bool:
        """
        CONSIGNA: True si en `fecha` el servicio esta activo Y dentro de
        su ventana [fecha_inicio, fecha_fin] (fecha_fin None = sin limite).

        Params: fecha (date)
        Retorno: bool
        """
        if not self.activo:
            return False
        if self.fecha_inicio and fecha < self.fecha_inicio:
            return False
        if self.fecha_fin and fecha > self.fecha_fin:
            return False
        return True

    def fecha_vencimiento_en(self, mes: int, anio: int) -> date:
        """
        CONSIGNA: construir la fecha de vencimiento de este servicio para
        el periodo (mes, anio). Ojo con dia_vencimiento = 31 en meses de
        28/29/30 dias: decidi la politica (ultimo dia del mes, etc.).

        Params: mes (1..12), anio (int)
        Retorno: date
        """
        ultimo_dia = monthrange(anio,mes)[1]
        return date(anio,mes,min(self.dia_vencimiento,ultimo_dia))


    def dias_para_vencimiento(self, fecha_ref: date) -> int:
        """
        CONSIGNA: dias entre `fecha_ref` y el proximo vencimiento del
        servicio. Sirve para decidir si toca generar una alerta.

        Params: fecha_ref (date)
        Retorno: int (puede ser negativo si ya vencio)
        """
        venc = self.fecha_vencimiento_en(fecha_ref.month, fecha_ref.year)
        return (venc - fecha_ref).days

    def debe_generar_alerta(self, fecha_ref: date) -> bool:
        """
        CONSIGNA: True si, parado en `fecha_ref`, faltan exactamente
        `dias_anticipacion_alerta` dias para el vencimiento. Es la parte
        "de la entidad" de la logica del generador de alertas (vista E /
        query comentada al final de 01_schema.sql). El "y ademas no se
        pago todavia este mes" lo agrega el caso de uso del modulo alertas.

        Params: fecha_ref (date)
        Retorno: bool
        """
        if not self.esta_vigente(fecha_ref):
            return False

        return self.dias_para_vencimiento(fecha_ref) == self.dias_anticipacion_alerta
