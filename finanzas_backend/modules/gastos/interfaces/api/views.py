"""
Vistas DRF del modulo gastos. Traducen HTTP <-> casos de uso; sin logica
de negocio ni ORM. Los casos de uso que cruzan modulos
(CalcularBalanceMensualUseCase, SimularModoEmergenciaUseCase) se arman
aca inyectando los repos concretos de cada modulo.
"""
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from modules.catalogos.infrastructure.repositories import DjangoNivelPrioridadRepository
from modules.gastos.application.use_cases.calcular_balance_mensual import (
    CalcularBalanceMensualUseCase,
)
from modules.gastos.application.use_cases.calcular_variacion_servicios import (
    CalcularVariacionServiciosUseCase,
)
from modules.gastos.application.use_cases.listar_gastos_del_periodo import (
    ListarGastosDelPeriodoUseCase,
)
from modules.gastos.application.use_cases.registrar_gasto import RegistrarGastoUseCase
from modules.gastos.application.use_cases.registrar_pago_servicio_fijo import (
    RegistrarPagoDeServicioFijoUseCase,
)
from modules.gastos.application.use_cases.simular_modo_emergencia import (
    SimularModoEmergenciaUseCase,
)
from modules.gastos.domain.exceptions import (
    EstadoGastoInvalido,
    MontoInvalido,
    PagoDeServicioDuplicado,
)
from modules.gastos.infrastructure.repositories import DjangoGastoRepository
from modules.gastos.interfaces.api.serializers import (
    AhorroPorPrioridadSerializer,
    BalanceMensualSerializer,
    GastoSerializer,
    RegistrarPagoServicioFijoSerializer,
    VariacionServicioSerializer,
    AhorroEmergenciaSerializer
)
from modules.ingresos.infrastructure.repositories import DjangoIngresoRepository

from modules.ingresos.interfaces.api.views import leer_periodo
from modules.servicios_fijos.infrastructure.repositories import DjangoServicioFijoRepository

PARAMS_PERIODO = [
    OpenApiParameter("mes", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True, description="Mes del periodo (1-12)."),
    OpenApiParameter("anio", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True, description="Año del periodo."),
]


class GastosView(APIView):
    """GET: gastos del usuario en un periodo (?mes=&anio=). POST: gasto puntual."""

    @extend_schema(
        tags=["Gastos"],
        summary="Listar gastos del periodo",
        description="Gastos del usuario autenticado en el periodo (mes, año) indicado (puntuales y pagos de servicio fijo).",
        parameters=PARAMS_PERIODO,
        responses=GastoSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
            mes, anio = leer_periodo(request)     # helper de ingresos/SOLUCION.txt
            caso = ListarGastosDelPeriodoUseCase(repositorio=DjangoGastoRepository())
            return Response(GastoSerializer(caso.ejecutar(request.user.id, mes, anio), many=True).data)

    @extend_schema(
        tags=["Gastos"],
        summary="Registrar un gasto puntual",
        description="Da de alta un gasto NO ligado a un servicio fijo (mercado, salidas, compras varias).",
        request=GastoSerializer,
        responses={
            201: GastoSerializer,
            400: OpenApiResponse(description="Monto o estado inválido."),
        },
    )
    def post(self, request: Request) -> Response:
        e = GastoSerializer(data=request.data)
        e.is_valid(raise_exception=True)
        caso = RegistrarGastoUseCase(repositorio=DjangoGastoRepository())
        try:
            gasto = caso.ejecutar(
                usuario_id=request.user.id,
                categoria_id=e.validated_data["categoria_id"],
                prioridad_id=e.validated_data["prioridad_id"],
                monto=e.validated_data["monto"],
                fecha_gasto=e.validated_data["fecha_gasto"],
                periodo_mes=e.validated_data["periodo_mes"],
                periodo_anio=e.validated_data["periodo_anio"],
                estado=e.validated_data.get("estado", "Pagado"),
                descripcion=e.validated_data.get("descripcion"),
            )
        except (MontoInvalido, EstadoGastoInvalido) as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(GastoSerializer(gasto).data, status=status.HTTP_201_CREATED)

class PagosServicioFijoView(APIView):
    """POST: registra el pago mensual de un servicio fijo."""

    @extend_schema(
        tags=["Gastos"],
        summary="Registrar pago de un servicio fijo",
        description="Registra el pago de un servicio fijo para un periodo (categoría/prioridad se deducen del propio servicio).",
        request=RegistrarPagoServicioFijoSerializer,
        responses={
            201: GastoSerializer,
            400: OpenApiResponse(description="Monto inválido."),
            404: OpenApiResponse(description="servicio_fijo_id inexistente."),
            409: OpenApiResponse(description="Ya existe un pago de ese servicio en ese periodo."),
        },
    )
    def post(self, request: Request) -> Response:
            e = RegistrarPagoServicioFijoSerializer(data=request.data)
            e.is_valid(raise_exception=True)
            # deducir categoria/prioridad del servicio fijo:
            servicio = DjangoServicioFijoRepository().obtener_por_id(
                e.validated_data["servicio_fijo_id"])
            if servicio is None:
                return Response({"detail": "servicio_fijo_id inexistente"}, status=404)
            caso = RegistrarPagoDeServicioFijoUseCase(repositorio=DjangoGastoRepository())
            try:
                gasto = caso.ejecutar(
                    usuario_id=request.user.id,
                    servicio_fijo_id=servicio.id,
                    categoria_id=servicio.categoria_id,
                    prioridad_id=servicio.prioridad_id,
                    monto=e.validated_data["monto"],
                    fecha_gasto=e.validated_data["fecha_gasto"],
                    periodo_mes=e.validated_data["periodo_mes"],
                    periodo_anio=e.validated_data["periodo_anio"],
                    descripcion=e.validated_data.get("descripcion"),
                )
            except PagoDeServicioDuplicado as ex:
                return Response({"detail": str(ex)}, status=status.HTTP_409_CONFLICT)
            except MontoInvalido as ex:
                return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(GastoSerializer(gasto).data, status=status.HTTP_201_CREATED)


class BalanceMensualView(APIView):
    """GET: balance (ingresos - gastos) del usuario en un periodo (?mes=&anio=)."""

    @extend_schema(
        tags=["Gastos"],
        summary="Balance mensual",
        description="total_ingresos - total_gastos del usuario autenticado en el periodo indicado.",
        parameters=PARAMS_PERIODO,
        responses=BalanceMensualSerializer,
    )
    def get(self, request: Request) -> Response:
            mes, anio = leer_periodo(request)
            caso = CalcularBalanceMensualUseCase(
                ingreso_repositorio=DjangoIngresoRepository(),
                gasto_repositorio=DjangoGastoRepository(),
            )
            return Response(BalanceMensualSerializer(caso.ejecutar(request.user.id, mes, anio)).data)


class VariacionServiciosView(APIView):
    """GET: variacion mes a mes del monto de un servicio fijo (?servicio_fijo_id=)."""

    @extend_schema(
        tags=["Gastos"],
        summary="Variación mes a mes de un servicio fijo",
        description="Por cada periodo pagado de un servicio fijo, el % de variación respecto al pago anterior.",
        parameters=[
            OpenApiParameter("servicio_fijo_id", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True),
        ],
        responses=VariacionServicioSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
            try:
                servicio_fijo_id = int(request.query_params["servicio_fijo_id"])
            except (KeyError, ValueError):
                return Response({"detail": "servicio_fijo_id requerido"}, status=400)
            caso = CalcularVariacionServiciosUseCase(repositorio=DjangoGastoRepository(),servicio_fijo_repositorio=DjangoServicioFijoRepository())
            return Response(VariacionServicioSerializer(caso.ejecutar(servicio_fijo_id), many=True).data)


class ModoEmergenciaView(APIView):
    """GET: ahorro potencial por prioridad del usuario en un periodo (?mes=&anio=)."""

    @extend_schema(
        tags=["Gastos"],
        summary="Simular modo emergencia",
        description="Gasto por prioridad del periodo y ahorro acumulado si se suspenden los gastos más prescindibles.",
        parameters=PARAMS_PERIODO,
        responses=AhorroEmergenciaSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
            mes, anio = leer_periodo(request)
            caso = SimularModoEmergenciaUseCase(
                gasto_repositorio=DjangoGastoRepository(),
                nivel_prioridad_repositorio=DjangoNivelPrioridadRepository(),
            )
            return Response(AhorroEmergenciaSerializer(caso.ejecutar(request.user.id, mes, anio), many=True).data)
