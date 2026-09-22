"""
Vistas DRF del modulo ingresos. Traducen HTTP <-> casos de uso; sin
logica de negocio ni ORM. Mismo molde que catalogos: armar caso de uso +
repo -> ejecutar con datos del request -> serializar.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from modules.ingresos.application.use_cases.calcular_total_ingresos_periodo import (
    CalcularTotalIngresosPeriodoUseCase,
)
from modules.ingresos.application.use_cases.listar_ingresos_del_periodo import (
    ListarIngresosDelPeriodoUseCase,
)
from modules.ingresos.application.use_cases.registrar_ingreso import (
    RegistrarIngresoUseCase,
)
from modules.ingresos.domain.exceptions import MontoInvalido, PeriodoInvalido
from modules.ingresos.infrastructure.repositories import DjangoIngresoRepository
from modules.ingresos.interfaces.api.serializers import (
    IngresoSerializer,
    TotalIngresosPeriodoSerializer,
)

from rest_framework.exceptions import ValidationError

def leer_periodo(request):
        try:
            return int(request.query_params["mes"]), int(request.query_params["anio"])
        except (KeyError, ValueError):
            raise ValidationError("Parametros 'mes' y 'anio' requeridos (enteros).")

PARAMS_PERIODO = [
    OpenApiParameter("mes", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True, description="Mes del periodo (1-12)."),
    OpenApiParameter("anio", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True, description="Año del periodo."),
]


class IngresosView(APIView):
    """GET: lista ingresos del usuario en un periodo (?mes=&anio=). POST: crea uno."""

    @extend_schema(
        tags=["Ingresos"],
        summary="Listar ingresos del periodo",
        description="Ingresos del usuario autenticado en el periodo (mes, año) indicado, ordenados por fecha.",
        parameters=PARAMS_PERIODO,
        responses=IngresoSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        mes,anio = leer_periodo(request)
        caso = ListarIngresosDelPeriodoUseCase(repositorio=DjangoIngresoRepository())
        datos = caso.ejecutar(request.user.id,mes,anio)
        return Response(IngresoSerializer(datos,many=True).data)


    @extend_schema(
        tags=["Ingresos"],
        summary="Registrar un ingreso",
        description="Da de alta un ingreso del usuario autenticado en un periodo.",
        request=IngresoSerializer,
        responses={
            201: IngresoSerializer,
            400: OpenApiResponse(description="Monto o periodo inválido."),
        },
    )
    def post(self, request: Request) -> Response:
        entrada = IngresoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        caso = RegistrarIngresoUseCase(repositorio=DjangoIngresoRepository())
        try:
            ingreso = caso.ejecutar(
                usuario_id=request.user.id,
                monto = entrada.validated_data["monto"],
                fecha = entrada.validated_data["fecha"],
                periodo_mes=entrada.validated_data["periodo_mes"],
                periodo_anio=entrada.validated_data["periodo_anio"],
                fuente=entrada.validated_data.get("fuente"),
                descripcion=entrada.validated_data.get("descripcion"),
            )
        except (MontoInvalido, PeriodoInvalido) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(IngresoSerializer(ingreso).data, status=status.HTTP_201_CREATED)


class TotalIngresosPeriodoView(APIView):
    """GET: total de ingresos del usuario en un periodo (?mes=&anio=)."""

    @extend_schema(
        tags=["Ingresos"],
        summary="Total de ingresos del periodo",
        description="Suma de los ingresos del usuario autenticado en el periodo (mes, año) indicado.",
        parameters=PARAMS_PERIODO,
        responses=TotalIngresosPeriodoSerializer,
    )
    def get(self, request: Request) -> Response:
        mes,anio = leer_periodo(request)
        caso = CalcularTotalIngresosPeriodoUseCase(repositorio=DjangoIngresoRepository())
        total = caso.ejecutar(request.user.id,mes,anio)

        return Response(TotalIngresosPeriodoSerializer({
            "periodo_mes":mes, "periodo_anio":anio, "total_ingresos":total
        }).data)

