"""
Serializers DRF del modulo planes_financieros. serializers.Serializer
simples (no ModelSerializer): describen la ENTIDAD DE DOMINIO
PlanFinanciero / el objeto de lectura ComparativaPlanVsReal. Ver el
porque en modules/catalogos/interfaces/api/serializers.py.
"""

from rest_framework import serializers


class PlanFinancieroSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    usuario_id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100, default="Mi plan")
    porcentaje_gasto_fijo = serializers.DecimalField(max_digits=5, decimal_places=2)
    porcentaje_ahorro = serializers.DecimalField(max_digits=5, decimal_places=2)
    porcentaje_gasto_libre = serializers.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = serializers.DateField(required=False)
    fecha_fin = serializers.DateField(required=False, allow_null=True)
    # required=False (no default): en el POST (crear) no se manda -> el
    # plan nace inactivo sin que este campo intervenga. En el PATCH
    # (actualizar) es opcional: si no viene, el caso de uso deja el
    # estado activo/inactivo tal cual estaba.
    activo = serializers.BooleanField(required=False)
    # TODO: [opcional: validar en .validate() que los 3 porcentajes sumen
    #        100 antes de llegar al caso de uso (defensa en profundidad).]


class ComparativaPlanVsRealSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    periodo_mes = serializers.IntegerField()
    periodo_anio = serializers.IntegerField()
    total_ingresos = serializers.DecimalField(max_digits=14, decimal_places=2)
    meta_gasto_fijo = serializers.DecimalField(max_digits=14, decimal_places=2)
    meta_ahorro = serializers.DecimalField(max_digits=14, decimal_places=2)
    meta_gasto_libre = serializers.DecimalField(max_digits=14, decimal_places=2)
    gasto_real = serializers.DecimalField(max_digits=14, decimal_places=2)
    balance_real = serializers.DecimalField(max_digits=14, decimal_places=2)
