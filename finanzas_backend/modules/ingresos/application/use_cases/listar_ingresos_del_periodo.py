"""Caso de uso: listar los ingresos de un usuario en un periodo."""

from dataclasses import dataclass

from modules.ingresos.domain.entities import Ingreso
from modules.ingresos.domain.ports.repositories import IngresoRepository


@dataclass
class ListarIngresosDelPeriodoUseCase:
    """
    El repositorio ya promete el orden por fecha; el caso de uso solo
    orquesta (mismo estilo que ListarCategoriasUseCase en catalogos).
    """

    repositorio: IngresoRepository

    def ejecutar(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> list[Ingreso]:
        """
        CONSIGNA: devolver los ingresos del usuario en (mes, anio).

        Retorno: list[Ingreso]
        """
        return self.repositorio.listar_por_usuario_y_periodo(usuario_id,periodo_mes,periodo_anio)
