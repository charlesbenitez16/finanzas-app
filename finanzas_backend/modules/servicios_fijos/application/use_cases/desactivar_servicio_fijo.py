"""Caso de uso: baja logica de un servicio fijo."""

from dataclasses import dataclass
from datetime import date

from modules.servicios_fijos.domain.entities import ServicioFijo
from modules.servicios_fijos.domain.exceptions import ServicioFijoNoEncontrado
from modules.servicios_fijos.domain.ports.repositories import ServicioFijoRepository


@dataclass
class DesactivarServicioFijoUseCase:
    """
    CONSIGNA
    --------
    Marca un servicio fijo como inactivo (activo = FALSE). Si el id no
    existe, lanzar ServicioFijoNoEncontrado. Pensa si ademas conviene
    setear fecha_fin = hoy.

    Params de ejecutar(): servicio_id: int
    Retorno: ServicioFijo (ya desactivado)
    """

    repositorio: ServicioFijoRepository

    def ejecutar(self, servicio_id: int) -> ServicioFijo:
        servicio = self.repositorio.obtener_por_id(servicio_id)
        if servicio is None:
            raise ServicioFijoNoEncontrado(f"No existe el servicio {servicio_id}")
        servicio.activo = False
        if servicio.fecha_fin is None:
            servicio.fecha_fin = date.today() 
        return self.repositorio.actualizar(servicio)
