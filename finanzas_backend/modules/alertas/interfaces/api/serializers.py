"""
Serializers DRF del modulo alertas. serializers.Serializer simples (no
ModelSerializer): describen la ENTIDAD DE DOMINIO AlertaPago. Ver el
porque en modules/catalogos/interfaces/api/serializers.py.
"""

from rest_framework import serializers


class AlertaPagoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    usuario_id = serializers.IntegerField(read_only=True)
    servicio_fijo_id = serializers.IntegerField()
    gasto_id = serializers.IntegerField(read_only=True, allow_null=True)
    periodo_mes = serializers.IntegerField(min_value=1, max_value=12)
    periodo_anio = serializers.IntegerField()
    fecha_alerta = serializers.DateField()
    estado = serializers.ChoiceField(
        choices=["Pendiente", "Enviada", "Leida", "Resuelta"], read_only=True
    )
    mensaje = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class CambiarEstadoAlertaSerializer(serializers.Serializer):
    """Entrada de PATCH /api/alertas/<id>/ : a que estado pasar."""

    estado = serializers.ChoiceField(choices=["Enviada", "Leida"])
    # TODO: [la vista mapea 'Enviada' -> MarcarAlertaComoEnviadaUseCase y
    #        'Leida' -> MarcarAlertaComoLeidaUseCase. 'Resuelta' NO se
    #        setea por API: sale del evento GastoRegistrado.]
