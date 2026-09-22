from django.contrib import admin

from modules.catalogos.infrastructure.models import CategoriaGastoModel, NivelPrioridadModel


@admin.register(CategoriaGastoModel)
class CategoriaGastoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "usuario", "icono")
    list_filter = ("usuario",)
    search_fields = ("nombre",)


@admin.register(NivelPrioridadModel)
class NivelPrioridadAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "nivel_orden")
    ordering = ("nivel_orden",)
