"""Excepciones de negocio del modulo gastos."""


class GastosError(Exception):
    """Excepcion base para errores de este modulo."""


class GastoNoEncontrado(GastosError):
    """Se intento operar sobre un gasto que no existe."""


class MontoInvalido(GastosError):
    """El monto no cumple el CHECK (monto > 0) del schema."""


class EstadoGastoInvalido(GastosError):
    """El estado no esta en ('Pagado', 'Pendiente', 'Vencido')."""


class PagoDeServicioDuplicado(GastosError):
    """
    Ya existe un pago registrado para ese servicio_fijo_id en ese
    (periodo_anio, periodo_mes). Viola uq_gasto_servicio_periodo.
    """


# TODO: [agrega mas excepciones a medida que aparezcan reglas.]
