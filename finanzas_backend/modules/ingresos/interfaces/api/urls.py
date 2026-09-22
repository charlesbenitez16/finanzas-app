from django.urls import path

from modules.ingresos.interfaces.api.views import (
    IngresosView,
    TotalIngresosPeriodoView,
)

urlpatterns = [
    path("", IngresosView.as_view(), name="ingresos"),
    path(
        "total-periodo/",
        TotalIngresosPeriodoView.as_view(),
        name="ingresos-total-periodo",
    ),
]
