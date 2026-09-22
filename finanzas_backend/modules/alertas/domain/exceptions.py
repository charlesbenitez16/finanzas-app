"""Excepciones de negocio del modulo alertas."""


class AlertasError(Exception):
    """Excepcion base para errores de este modulo."""


class AlertaNoEncontrada(AlertasError):
    """Se intento operar sobre una alerta que no existe."""


class AlertaDuplicada(AlertasError):
    """
    Ya existe una alerta para ese servicio_fijo_id en ese
    (periodo_anio, periodo_mes). Viola uq_alerta_servicio_periodo.
    """


class TransicionEstadoInvalida(AlertasError):
    """Se intento una transicion de estado que la maquina no permite."""


# TODO: [agrega mas excepciones a medida que aparezcan reglas.]
