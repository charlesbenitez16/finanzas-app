"""
Puertos del dominio de planes_financieros. Los implementa
infrastructure/repositories.py con Django ORM.
"""

from abc import ABC, abstractmethod
from typing import Optional

from modules.planes_financieros.domain.entities import PlanFinanciero


class PlanFinancieroRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, plan_id: int) -> Optional[PlanFinanciero]:
        """Devuelve el PlanFinanciero con ese id, o None."""
        ...

    @abstractmethod
    def crear(self, plan: PlanFinanciero) -> PlanFinanciero:
        """Persiste un PlanFinanciero nuevo y lo devuelve con id."""
        ...

    @abstractmethod
    def actualizar(self, plan: PlanFinanciero) -> PlanFinanciero:
        """Persiste cambios de un PlanFinanciero existente (ej. activar/desactivar)."""
        ...

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> list[PlanFinanciero]:
        """
        Todos los planes del usuario (activos e inactivos), mas nuevo primero.

        MAPEO SQL:
            SELECT * FROM plan_financiero WHERE usuario_id = %s
            ORDER BY fecha_inicio DESC
        """
        ...

    @abstractmethod
    def obtener_plan_activo(self, usuario_id: int) -> Optional[PlanFinanciero]:
        """
        MAPEO SQL -- lo que garantiza uq_plan_activo_usuario (indice
        parcial WHERE activo = TRUE) y lo que consume vista_plan_vs_real:
            SELECT * FROM plan_financiero
            WHERE usuario_id = %s AND activo = TRUE

        Retorno: el plan activo, o None si el usuario no tiene ninguno.
        """
        ...
