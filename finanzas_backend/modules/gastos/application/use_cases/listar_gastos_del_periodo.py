"""Caso de uso: listar los gastos de un usuario en un periodo."""

from dataclasses import dataclass

from modules.gastos.domain.entities import Gasto
from modules.gastos.domain.ports.repositories import GastoRepository


@dataclass
class ListarGastosDelPeriodoUseCase:
    repositorio: GastoRepository

    def ejecutar(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> list[Gasto]:
        """
        CONSIGNA: devolver los gastos del usuario en (mes, anio). El caso
        de uso solo orquesta (mismo estilo que ListarCategoriasUseCase en
        catalogos).

        Retorno: list[Gasto]
        """
        return self.repositorio.listar_por_usuario_y_periodo(usuario_id, periodo_mes, periodo_anio)
