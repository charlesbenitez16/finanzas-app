"""
Enrutador raiz del proyecto.

Cada modulo expone sus propias rutas en `modules/<modulo>/interfaces/api/urls.py`
y aqui solo se las incluye bajo su prefijo. El enrutador raiz nunca define
vistas propias: solo agrega las de cada modulo.
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # OpenAPI: esquema crudo + Swagger UI + ReDoc, generados a partir de
    # las vistas/serializers de cada modulo (ver @extend_schema en cada
    # interfaces/api/views.py).
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/catalogos/", include("modules.catalogos.interfaces.api.urls")),
    path("api/usuarios/", include("modules.usuarios.interfaces.api.urls")),
    path("api/ingresos/", include("modules.ingresos.interfaces.api.urls")),
    path("api/servicios-fijos/", include("modules.servicios_fijos.interfaces.api.urls")),
    path("api/gastos/", include("modules.gastos.interfaces.api.urls")),
    path(
        "api/planes-financieros/",
        include("modules.planes_financieros.interfaces.api.urls"),
    ),
    path("api/alertas/", include("modules.alertas.interfaces.api.urls")),
]
