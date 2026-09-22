"""
Serializers DRF del modulo ingresos. serializers.Serializer simples (no
ModelSerializer): describen la ENTIDAD DE DOMINIO Ingreso, no la tabla.
Ver el porque en modules/catalogos/interfaces/api/serializers.py.
"""

from rest_framework import serializers


class IngresoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    usuario_id = serializers.IntegerField(read_only=True)
    monto = serializers.DecimalField(max_digits=12, decimal_places=2)
    fecha = serializers.DateField()
    periodo_mes = serializers.IntegerField(min_value=1, max_value=12)
    periodo_anio = serializers.IntegerField()
    fuente = serializers.CharField(
        max_length=100, required=False, allow_null=True, allow_blank=True
    )
    descripcion = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )


class TotalIngresosPeriodoSerializer(serializers.Serializer):
    """Salida de GET /api/ingresos/total-periodo/."""

    periodo_mes = serializers.IntegerField()
    periodo_anio = serializers.IntegerField()
    total_ingresos = serializers.DecimalField(max_digits=14, decimal_places=2)
