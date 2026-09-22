from django.urls import path

from modules.planes_financieros.interfaces.api.views import (
    ActivarPlanView,
    ComparativaView,
    PlanDetalleView,
    PlanesFinancierosView,
)

urlpatterns = [
    path("", PlanesFinancierosView.as_view(), name="planes-financieros"),
    # PlanDetalleView es una vista APARTE (solo PATCH): ver el porque en
    # su docstring, en interfaces/api/views.py.
    path(
        "<int:plan_id>/",
        PlanDetalleView.as_view(),
        name="planes-financieros-detalle",
    ),
    path(
        "<int:plan_id>/activar/",
        ActivarPlanView.as_view(),
        name="planes-financieros-activar",
    ),
    path("comparativa/", ComparativaView.as_view(), name="planes-financieros-comparativa"),
]
