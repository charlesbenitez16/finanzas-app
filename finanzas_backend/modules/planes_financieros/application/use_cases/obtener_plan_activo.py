"""Caso de uso: obtener el plan financiero activo de un usuario."""

from dataclasses import dataclass
from typing import Optional

from modules.planes_financieros.domain.entities import PlanFinanciero
from modules.planes_financieros.domain.ports.repositories import (
    PlanFinancieroRepository,
)


@dataclass
class ObtenerPlanActivoUseCase:
    repositorio: PlanFinancieroRepository

    def ejecutar(self, usuario_id: int) -> Optional[PlanFinanciero]:
        """
        CONSIGNA: devolver el plan activo del usuario, o None. El caso de
        uso solo orquesta (mismo estilo que ListarCategoriasUseCase en
        catalogos).

        Retorno: Optional[PlanFinanciero]
        """
        return self.repositorio.obtener_plan_activo(usuario_id)
