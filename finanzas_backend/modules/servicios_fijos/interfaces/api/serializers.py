"""
Serializers DRF del modulo servicios_fijos. serializers.Serializer
simples (no ModelSerializer): describen la ENTIDAD DE DOMINIO
ServicioFijo. Ver el porque en
modules/catalogos/interfaces/api/serializers.py.
"""

from rest_framework import serializers


class ServicioFijoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    usuario_id = serializers.IntegerField(read_only=True)
    categoria_id = serializers.IntegerField()
    prioridad_id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=150)
    dia_vencimiento = serializers.IntegerField(min_value=1, max_value=31)
    monto_estimado = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )
    es_monto_variable = serializers.BooleanField(default=False)
    dias_anticipacion_alerta = serializers.IntegerField(default=3, min_value=0)
    activo = serializers.BooleanField(read_only=True)
    fecha_inicio = serializers.DateField(required=False)
    fecha_fin = serializers.DateField(required=False, allow_null=True)
    notas = serializers.CharField(required=False, allow_null=True, allow_blank=True)
