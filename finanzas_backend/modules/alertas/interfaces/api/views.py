"""
Vistas DRF del modulo alertas. Traducen HTTP <-> casos de uso; sin
logica de negocio ni ORM. GenerarAlertasDeVencimientoUseCase cruza con
servicios_fijos: se arma aca inyectando los dos repos concretos.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from modules.alertas.application.use_cases.generar_alertas_de_vencimiento import (
    GenerarAlertasDeVencimientoUseCase,
)
from modules.alertas.application.use_cases.listar_alertas_pendientes import (
    ListarAlertasPendientesUseCase,
)
from modules.alertas.application.use_cases.marcar_alerta import (
    MarcarAlertaComoEnviadaUseCase,
    MarcarAlertaComoLeidaUseCase,
)
from modules.alertas.domain.exceptions import (
    AlertaNoEncontrada,
    TransicionEstadoInvalida,
)
from modules.alertas.infrastructure.repositories import DjangoAlertaPagoRepository
from modules.alertas.interfaces.api.serializers import (
    AlertaPagoSerializer,
    CambiarEstadoAlertaSerializer,
)
from modules.servicios_fijos.infrastructure.repositories import (
    DjangoServicioFijoRepository,
)
from datetime import date

class AlertasView(APIView):
    """GET: alertas del usuario en un estado (?estado=Pendiente por defecto)."""

    @extend_schema(
        tags=["Alertas"],
        summary="Listar alertas por estado",
        description="Alertas del usuario autenticado en un estado dado (Pendiente/Enviada/Leida/Resuelta).",
        parameters=[
            OpenApiParameter(
                "estado", OpenApiTypes.STR, OpenApiParameter.QUERY, required=False,
                description="Pendiente (default) | Enviada | Leida | Resuelta.",
            ),
        ],
        responses=AlertaPagoSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
            estado = request.query_params.get("estado", "Pendiente")
            caso = ListarAlertasPendientesUseCase(repositorio=DjangoAlertaPagoRepository())
            return Response(AlertaPagoSerializer(
                caso.ejecutar(request.user.id, estado), many=True).data)


class GenerarAlertasView(APIView):
    """POST: corre el generador de alertas de vencimiento (endpoint del job/cron)."""

    @extend_schema(
        tags=["Alertas"],
        summary="Generar alertas de vencimiento",
        description=(
            "Crea alertas 'Pendiente' para los servicios fijos próximos a vencer "
            "(parado en `fecha`, por defecto hoy). Idempotente: no duplica alertas "
            "ya generadas para el mismo servicio/periodo."
        ),
        parameters=[
            OpenApiParameter(
                "fecha", OpenApiTypes.DATE, OpenApiParameter.QUERY, required=False,
                description="Fecha de referencia (YYYY-MM-DD). También se acepta en el body. Por defecto, hoy.",
            ),
        ],
        request=None,
        responses={201: AlertaPagoSerializer(many=True)},
    )
    def post(self, request: Request) -> Response:
            fecha_str = request.data.get("fecha") or request.query_params.get("fecha")
            fecha = date.fromisoformat(fecha_str) if fecha_str else None
            caso = GenerarAlertasDeVencimientoUseCase(
                servicio_fijo_repositorio=DjangoServicioFijoRepository(),
                alerta_repositorio=DjangoAlertaPagoRepository(),
            )
            creadas = caso.ejecutar(fecha)
            return Response(AlertaPagoSerializer(creadas, many=True).data,
                            status=status.HTTP_201_CREATED)


class AlertaDetailView(APIView):
    """PATCH /api/alertas/<alerta_id>/ : transicion de estado (Enviada / Leida)."""

    @extend_schema(
        tags=["Alertas"],
        summary="Cambiar estado de una alerta",
        description=(
            "Aplica una transición manual de estado: Pendiente -> Enviada, o "
            "Enviada -> Leida. 'Resuelta' no se setea por acá: ocurre sola cuando "
            "se registra el pago del servicio fijo correspondiente."
        ),
        request=CambiarEstadoAlertaSerializer,
        responses={
            200: AlertaPagoSerializer,
            404: OpenApiResponse(description="No existe la alerta."),
            409: OpenApiResponse(description="Transición de estado no permitida."),
        },
    )
    def patch(self, request: Request, alerta_id: int) -> Response:
            e = CambiarEstadoAlertaSerializer(data=request.data)
            e.is_valid(raise_exception=True)
            repo = DjangoAlertaPagoRepository()
            destino = e.validated_data["estado"]
            caso = (MarcarAlertaComoEnviadaUseCase(repositorio=repo)
                    if destino == "Enviada"
                    else MarcarAlertaComoLeidaUseCase(repositorio=repo))
            try:
                alerta = caso.ejecutar(alerta_id)
            except AlertaNoEncontrada as ex:
                return Response({"detail": str(ex)}, status=status.HTTP_404_NOT_FOUND)
            except TransicionEstadoInvalida as ex:
                return Response({"detail": str(ex)}, status=status.HTTP_409_CONFLICT)
            return Response(AlertaPagoSerializer(alerta).data)
