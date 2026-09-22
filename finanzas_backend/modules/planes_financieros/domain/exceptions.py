"""Excepciones de negocio del modulo planes_financieros."""


class PlanesFinancierosError(Exception):
    """Excepcion base para errores de este modulo."""


class PlanNoEncontrado(PlanesFinancierosError):
    """Se intento operar sobre un plan que no existe."""


class PorcentajesNoSuman100(PlanesFinancierosError):
    """gasto_fijo + ahorro + gasto_libre != 100 (CHECK del schema)."""


class YaExistePlanActivo(PlanesFinancierosError):
    """
    El usuario ya tiene un plan activo. Viola uq_plan_activo_usuario
    (indice parcial WHERE activo = TRUE). Debe desactivarse el anterior
    antes de activar otro.
    """


# TODO: [agrega mas excepciones a medida que aparezcan reglas.]
