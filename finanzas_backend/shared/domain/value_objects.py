"""Value objects reutilizables entre modulos."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Periodo:
    """Mes/anio de referencia para ingresos y gastos (ej. marzo 2026)."""

    mes: int
    anio: int

    def __post_init__(self) -> None:
        # TODO: validar que 1 <= mes <= 12 y que anio sea razonable
        # (ej. mayor a 2000). Si no se cumple, lanzar ValueError.
        raise NotImplementedError

    def __str__(self) -> str:
        # TODO: devolver una representacion legible, ej. "2026-03"
        raise NotImplementedError


@dataclass(frozen=True)
class Dinero:
    """Representa un monto monetario. Evita usar float directo para dinero."""

    monto: float

    def __post_init__(self) -> None:
        # TODO: validar que el monto no sea negativo (lanzar ValueError)
        raise NotImplementedError

    def porcentaje_de_variacion_respecto_a(self, monto_anterior: "Dinero") -> float:
        # TODO: calcular el % de variacion respecto a un monto anterior.
        # Es la misma logica que ya implementamos en SQL con LAG, pero
        # ahora en Python puro.
        raise NotImplementedError
