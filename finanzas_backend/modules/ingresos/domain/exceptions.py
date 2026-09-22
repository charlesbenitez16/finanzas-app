"""Excepciones de negocio del modulo ingresos."""


class IngresosError(Exception):
    """Excepcion base para errores de este modulo."""


class IngresoNoEncontrado(IngresosError):
    """Se intento operar sobre un ingreso que no existe."""


class MontoInvalido(IngresosError):
    """El monto no cumple el CHECK (monto > 0) del schema."""


class PeriodoInvalido(IngresosError):
    """periodo_mes fuera de 1..12, o periodo_anio no razonable."""


# TODO: [agrega mas excepciones a medida que aparezcan reglas.]
