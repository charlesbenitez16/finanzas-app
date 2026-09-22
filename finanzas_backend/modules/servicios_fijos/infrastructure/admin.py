from django.contrib import admin

from modules.servicios_fijos.infrastructure.models import ServicioFijoModel


@admin.register(ServicioFijoModel)
class ServicioFijoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "usuario",
        "dia_vencimiento",
        "monto_estimado",
        "es_monto_variable",
        "activo",
    )
    list_filter = ("activo", "es_monto_variable", "prioridad")
    search_fields = ("nombre", "notas")
