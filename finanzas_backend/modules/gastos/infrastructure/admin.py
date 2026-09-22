from django.contrib import admin

from modules.gastos.infrastructure.models import GastoModel


@admin.register(GastoModel)
class GastoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "monto",
        "fecha_gasto",
        "periodo_mes",
        "periodo_anio",
        "estado",
        "servicio_fijo",
    )
    list_filter = ("estado", "periodo_anio", "periodo_mes", "prioridad")
    search_fields = ("descripcion",)
