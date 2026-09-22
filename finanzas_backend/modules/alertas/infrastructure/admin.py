from django.contrib import admin

from modules.alertas.infrastructure.models import AlertaPagoModel


@admin.register(AlertaPagoModel)
class AlertaPagoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "servicio_fijo",
        "periodo_mes",
        "periodo_anio",
        "fecha_alerta",
        "estado",
        "gasto",
    )
    list_filter = ("estado", "periodo_anio", "periodo_mes")
    search_fields = ("mensaje",)
