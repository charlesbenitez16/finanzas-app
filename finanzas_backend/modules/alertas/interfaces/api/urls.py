from django.urls import path

from modules.alertas.interfaces.api.views import (
    AlertaDetailView,
    AlertasView,
    GenerarAlertasView,
)

urlpatterns = [
    path("", AlertasView.as_view(), name="alertas"),
    path("generar/", GenerarAlertasView.as_view(), name="alertas-generar"),
    path("<int:alerta_id>/", AlertaDetailView.as_view(), name="alertas-detalle"),
]
