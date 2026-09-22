from django.urls import path

from modules.servicios_fijos.interfaces.api.views import (
    ServiciosFijosView,
    ServiciosProximosAVencerView,
)

urlpatterns = [
    path("", ServiciosFijosView.as_view(), name="servicios-fijos"),
    path(
        "proximos-a-vencer/",
        ServiciosProximosAVencerView.as_view(),
        name="servicios-fijos-proximos-a-vencer",
    ),
]
