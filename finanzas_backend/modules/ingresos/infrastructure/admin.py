from django.contrib import admin

from modules.ingresos.infrastructure.models import IngresoModel


@admin.register(IngresoModel)
class IngresoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "monto",
        "fecha",
        "periodo_mes",
        "periodo_anio",
        "fuente",
    )
    list_filter = ("periodo_anio", "periodo_mes", "fuente")
    search_fields = ("descripcion", "fuente")
