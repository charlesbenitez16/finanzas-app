from django.urls import path

from modules.gastos.interfaces.api.views import (
    BalanceMensualView,
    GastosView,
    ModoEmergenciaView,
    PagosServicioFijoView,
    VariacionServiciosView,
)

urlpatterns = [
    path("", GastosView.as_view(), name="gastos"),
    path("pagos-servicio/", PagosServicioFijoView.as_view(), name="gastos-pago-servicio"),
    path("balance-mensual/", BalanceMensualView.as_view(), name="gastos-balance-mensual"),
    path(
        "variacion-servicios/",
        VariacionServiciosView.as_view(),
        name="gastos-variacion-servicios",
    ),
    path("modo-emergencia/", ModoEmergenciaView.as_view(), name="gastos-modo-emergencia"),
]
