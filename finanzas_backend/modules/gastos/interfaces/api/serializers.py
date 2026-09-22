"""
Serializers DRF del modulo gastos. serializers.Serializer simples (no
ModelSerializer): describen entidades / objetos de lectura del dominio,
no la tabla. Ver el porque en
modules/catalogos/interfaces/api/serializers.py.
"""

from rest_framework import serializers


class GastoSerializer(serializers.Serializer):
    """Salida generica de un Gasto y entrada de un gasto puntual."""

    id = serializers.IntegerField(read_only=True)
    usuario_id = serializers.IntegerField(read_only=True)
    categoria_id = serializers.IntegerField()
    servicio_fijo_id = serializers.IntegerField(
        required=False, allow_null=True, read_only=True
    )
    prioridad_id = serializers.IntegerField()
    monto = serializers.DecimalField(max_digits=12, decimal_places=2)
    fecha_gasto = serializers.DateField()
    periodo_mes = serializers.IntegerField(min_value=1, max_value=12)
    periodo_anio = serializers.IntegerField()
    estado = serializers.ChoiceField(
        choices=["Pagado", "Pendiente", "Vencido"], default="Pagado"
    )
    descripcion = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )


class RegistrarPagoServicioFijoSerializer(serializers.Serializer):
    """
    Entrada de POST /api/gastos/pagos-servicio/. categoria_id y
    prioridad_id NO van acá: la vista los deduce del propio servicio
    fijo (servicio.categoria_id / servicio.prioridad_id).
    """

    servicio_fijo_id = serializers.IntegerField()
    monto = serializers.DecimalField(max_digits=12, decimal_places=2)
    fecha_gasto = serializers.DateField()
    periodo_mes = serializers.IntegerField(min_value=1, max_value=12)
    periodo_anio = serializers.IntegerField()
    descripcion = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )


class BalanceMensualSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    periodo_mes = serializers.IntegerField()
    periodo_anio = serializers.IntegerField()
    total_ingresos = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_gastos = serializers.DecimalField(max_digits=14, decimal_places=2)
    balance = serializers.DecimalField(max_digits=14, decimal_places=2)


class VariacionServicioSerializer(serializers.Serializer):
    servicio_fijo_id = serializers.IntegerField()
    servicio = serializers.CharField()
    periodo_mes = serializers.IntegerField()
    periodo_anio = serializers.IntegerField()
    monto_actual = serializers.DecimalField(max_digits=12, decimal_places=2)
    monto_anterior = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True
    )
    porcentaje_variacion = serializers.DecimalField(
        max_digits=7, decimal_places=2, allow_null=True
    )


class AhorroPorPrioridadSerializer(serializers.Serializer):
    prioridad = serializers.CharField()
    nivel_orden = serializers.IntegerField()
    total_por_prioridad = serializers.DecimalField(max_digits=14, decimal_places=2)
    # TODO: [agrega aca el campo de ahorro acumulado que definas en
    #        SimularModoEmergenciaUseCase.]

class AhorroEmergenciaSerializer(serializers.Serializer):
        prioridad = serializers.CharField()
        nivel_orden = serializers.IntegerField()
        total_periodo = serializers.DecimalField(max_digits=14, decimal_places=2)
        ahorro_acumulado_si_suspende = serializers.DecimalField(max_digits=14, decimal_places=2)