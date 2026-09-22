from django.contrib import admin

from modules.planes_financieros.infrastructure.models import PlanFinancieroModel


@admin.register(PlanFinancieroModel)
class PlanFinancieroAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "usuario",
        "porcentaje_gasto_fijo",
        "porcentaje_ahorro",
        "porcentaje_gasto_libre",
        "activo",
        "fecha_inicio",
    )
    list_filter = ("activo",)
    search_fields = ("nombre",)
