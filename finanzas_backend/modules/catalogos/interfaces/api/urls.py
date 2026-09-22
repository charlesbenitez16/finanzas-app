from django.urls import path

from modules.catalogos.interfaces.api.views import CategoriasGastoView, NivelesPrioridadView

urlpatterns = [
    path("categorias/", CategoriasGastoView.as_view(), name="categorias-gasto"),
    path("niveles-prioridad/", NivelesPrioridadView.as_view(), name="niveles-prioridad"),
]
