"""Excepciones de negocio del modulo servicios_fijos."""


class ServiciosFijosError(Exception):
    """Excepcion base para errores de este modulo."""


class ServicioFijoNoEncontrado(ServiciosFijosError):
    """Se intento operar sobre un servicio fijo que no existe."""


class DiaVencimientoInvalido(ServiciosFijosError):
    """dia_vencimiento fuera de 1..31 (CHECK del schema)."""


class RangoFechasInvalido(ServiciosFijosError):
    """fecha_fin es anterior a fecha_inicio."""


class MontoEstimadoInvalido(ServiciosFijosError):
    """monto_estimado negativo (CHECK monto_estimado >= 0)."""


# TODO: [agrega mas excepciones a medida que aparezcan reglas.]
