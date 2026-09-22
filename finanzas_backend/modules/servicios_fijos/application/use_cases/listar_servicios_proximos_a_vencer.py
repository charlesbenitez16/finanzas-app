"""Caso de uso: listar servicios fijos proximos a vencer (insumo del generador de alertas)."""

from dataclasses import dataclass
from datetime import date

from modules.servicios_fijos.domain.entities import ServicioFijo
from modules.servicios_fijos.domain.ports.repositories import ServicioFijoRepository


@dataclass
class ListarServiciosProximosAVencerUseCase:
    """
    CONSIGNA
    --------
    Devuelve los servicios fijos activos cuyo vencimiento cae dentro de
    su ventana de anticipacion (`dias_anticipacion_alerta`), parado en
    `fecha_referencia`. Es la parte de este modulo de la query comentada
    al final de 01_schema.sql (vista E). El modulo `alertas` toma esta
    lista y, para cada servicio, verifica que no exista ya el pago del
    mes ni una alerta previa antes de crear la alerta.

    Params de ejecutar(): fecha_referencia: date (default: hoy)
    Retorno: list[ServicioFijo]
    """

    repositorio: ServicioFijoRepository

    def ejecutar(self, fecha_referencia: date | None = None) -> list[ServicioFijo]:
        return self.repositorio.listar_proximos_a_vencer(fecha_referencia or date.today())
