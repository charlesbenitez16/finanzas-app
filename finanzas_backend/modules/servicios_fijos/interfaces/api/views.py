"""
Vistas DRF del modulo servicios_fijos. Traducen HTTP <-> casos de uso;
sin logica de negocio ni ORM. Mismo molde que catalogos.
"""

from datetime import date

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from modules.servicios_fijos.application.use_cases.crear_servicio_fijo import (
    CrearServicioFijoUseCase,
)
from modules.servicios_fijos.application.use_cases.listar_servicios_activos import (
    ListarServiciosActivosUseCase,
)
from modules.servicios_fijos.application.use_cases.listar_servicios_proximos_a_vencer import (
    ListarServiciosProximosAVencerUseCase,
)
from modules.servicios_fijos.domain.exceptions import (
    DiaVencimientoInvalido,
    MontoEstimadoInvalido,
    RangoFechasInvalido,
)
from modules.servicios_fijos.infrastructure.repositories import (
    DjangoServicioFijoRepository,
)
from modules.servicios_fijos.interfaces.api.serializers import ServicioFijoSerializer


class ServiciosFijosView(APIView):
    """GET: lista los servicios fijos activos del usuario. POST: crea uno."""

    @extend_schema(
        tags=["Servicios Fijos"],
        summary="Listar servicios fijos activos",
        description="Servicios fijos activos (activo=True) del usuario autenticado, ordenados por nombre.",
        responses=ServicioFijoSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        caso = ListarServiciosActivosUseCase(repositorio=DjangoServicioFijoRepository())
        return Response(ServicioFijoSerializer(caso.ejecutar(request.user.id), many=True).data)

    @extend_schema(
        tags=["Servicios Fijos"],
        summary="Crear servicio fijo",
        description="Da de alta un servicio fijo / gasto recurrente (ej. Internet, Agua, Gimnasio).",
        request=ServicioFijoSerializer,
        responses={
            201: ServicioFijoSerializer,
            400: OpenApiResponse(description="dia_vencimiento, monto_estimado o rango de fechas inválido."),
        },
    )
    def post(self, request: Request) -> Response:
        entrada = ServicioFijoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        caso = CrearServicioFijoUseCase(repositorio=DjangoServicioFijoRepository())
        try:
                servicio = caso.ejecutar(
                    usuario_id=request.user.id,
                    categoria_id=entrada.validated_data["categoria_id"],
                    prioridad_id=entrada.validated_data["prioridad_id"],
                    nombre=entrada.validated_data["nombre"],
                    dia_vencimiento=entrada.validated_data["dia_vencimiento"],
                    monto_estimado=entrada.validated_data.get("monto_estimado"),
                    es_monto_variable=entrada.validated_data.get("es_monto_variable", False),
                    dias_anticipacion_alerta=entrada.validated_data.get("dias_anticipacion_alerta", 3),
                    fecha_inicio=entrada.validated_data.get("fecha_inicio"),
                    fecha_fin=entrada.validated_data.get("fecha_fin"),
                    notas=entrada.validated_data.get("notas"),
                )
        except (DiaVencimientoInvalido, MontoEstimadoInvalido, RangoFechasInvalido) as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ServicioFijoSerializer(servicio).data, status=status.HTTP_201_CREATED)


class ServiciosProximosAVencerView(APIView):
    """GET: servicios fijos proximos a vencer (?fecha=YYYY-MM-DD opcional)."""

    @extend_schema(
        tags=["Servicios Fijos"],
        summary="Servicios próximos a vencer",
        description=(
            "Servicios fijos activos cuyo vencimiento cae dentro de su ventana de "
            "anticipación, parado en `fecha` (por defecto, hoy). Insumo del generador de alertas."
        ),
        parameters=[
            OpenApiParameter(
                "fecha", OpenApiTypes.DATE, OpenApiParameter.QUERY, required=False,
                description="Fecha de referencia (YYYY-MM-DD). Por defecto, hoy.",
            ),
        ],
        responses=ServicioFijoSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        fecha_str = request.query_params.get("fecha")
        fecha = date.fromisoformat(fecha_str) if fecha_str else None
        caso = ListarServiciosProximosAVencerUseCase(repositorio=DjangoServicioFijoRepository())
        return Response(ServicioFijoSerializer(caso.ejecutar(fecha), many=True).data)
