"""
Vistas DRF del modulo planes_financieros. Traducen HTTP <-> casos de
uso; sin logica de negocio ni ORM. CompararPlanVsRealUseCase se arma
aca inyectandole el CalcularBalanceMensualUseCase ya construido con los
repos concretos de ingresos y gastos.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from modules.ingresos.interfaces.api.views import leer_periodo
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from modules.gastos.application.use_cases.calcular_balance_mensual import (
    CalcularBalanceMensualUseCase,
)
from modules.gastos.infrastructure.repositories import DjangoGastoRepository
from modules.ingresos.infrastructure.repositories import DjangoIngresoRepository
from modules.planes_financieros.application.use_cases.activar_plan_financiero import (
    ActivarPlanFinancieroUseCase,
)
from modules.planes_financieros.application.use_cases.comparar_plan_vs_real import (
    CompararPlanVsRealUseCase,
)
from modules.planes_financieros.application.use_cases.crear_plan_financiero import (
    CrearPlanFinancieroUseCase,
)
from modules.planes_financieros.application.use_cases.actualizar_plan_financiero import (
    ActualizarPlanFinancieroUseCase,
)
from modules.planes_financieros.application.use_cases.obtener_plan_activo import (
    ObtenerPlanActivoUseCase,
)
from modules.planes_financieros.domain.exceptions import (
    PlanNoEncontrado,
    PorcentajesNoSuman100,
    YaExistePlanActivo,
)
from modules.planes_financieros.infrastructure.repositories import (
    DjangoPlanFinancieroRepository,
)
from modules.planes_financieros.interfaces.api.serializers import (
    ComparativaPlanVsRealSerializer,
    PlanFinancieroSerializer,
)


class PlanesFinancierosView(APIView):
    """GET: planes del usuario. POST: crea un plan."""

    @extend_schema(
        tags=["Planes Financieros"],
        summary="Listar planes financieros",
        description="Todos los planes (activos e inactivos) del usuario autenticado, más nuevo primero.",
        responses=PlanFinancieroSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        repo = DjangoPlanFinancieroRepository()
        planes = repo.listar_por_usuario(request.user.id)
        return Response(PlanFinancieroSerializer(planes, many=True).data)

    @extend_schema(
        tags=["Planes Financieros"],
        summary="Crear plan financiero",
        description="Crea un plan (nace inactivo). Los 3 porcentajes deben sumar 100.",
        request=PlanFinancieroSerializer,
        responses={
            201: PlanFinancieroSerializer,
            400: OpenApiResponse(description="Los porcentajes no suman 100."),
        },
    )
    def post(self, request: Request) -> Response:
            e = PlanFinancieroSerializer(data=request.data); e.is_valid(raise_exception=True)
            caso = CrearPlanFinancieroUseCase(repositorio=DjangoPlanFinancieroRepository())
            try:
                plan = caso.ejecutar(
                    usuario_id=request.user.id,
                    porcentaje_gasto_fijo=e.validated_data["porcentaje_gasto_fijo"],
                    porcentaje_ahorro=e.validated_data["porcentaje_ahorro"],
                    porcentaje_gasto_libre=e.validated_data["porcentaje_gasto_libre"],
                    nombre=e.validated_data.get("nombre", "Mi plan"),
                    fecha_inicio=e.validated_data.get("fecha_inicio"),
                    fecha_fin=e.validated_data.get("fecha_fin"),
                )
            except PorcentajesNoSuman100 as ex:
                return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(PlanFinancieroSerializer(plan).data, status=status.HTTP_201_CREATED)


class PlanDetalleView(APIView):
    """
    PATCH /api/planes-financieros/<plan_id>/.

    Vista APARTE de PlanesFinancierosView (no metodo agregado a esa
    clase) a proposito: PlanesFinancierosView.get()/post() no reciben
    plan_id en su firma. Si esta misma vista se mapeara TAMBIEN en la URL
    "<int:plan_id>/", Django le pasaria plan_id como kwarg a get()/post()
    igual y explotarian con TypeError (500) apenas alguien pegara un GET
    o POST a esa URL con id. Con una clase propia, esa URL solo entiende
    PATCH y el resto de metodos HTTP dan 405 (Method Not Allowed), que es
    lo esperable.
    """

    @extend_schema(
            tags=["Planes Financieros"],
            summary="Actualizar plan financiero",
            description=(
                "Actualiza el plan `plan_id` del usuario autenticado. Los 3 "
                "porcentajes deben sumar 100. Si se manda activo=true y había "
                "otro plan activo, ese otro se desactiva primero (misma regla "
                "que /activar/)."
            ),
            request=PlanFinancieroSerializer,
            responses={
                200: PlanFinancieroSerializer,
                400: OpenApiResponse(description="Los porcentajes no suman 100."),
                404: OpenApiResponse(description="No existe ese plan para este usuario."),
            },
    )
    def patch(self, request: Request, plan_id: int) -> Response:
        e = PlanFinancieroSerializer(data=request.data); e.is_valid(raise_exception=True)
        caso = ActualizarPlanFinancieroUseCase(repositorio=DjangoPlanFinancieroRepository())
        try:
            plan = caso.ejecutar(
                plan_id=plan_id,
                usuario_id=request.user.id,
                porcentaje_gasto_fijo=e.validated_data["porcentaje_gasto_fijo"],
                porcentaje_ahorro=e.validated_data["porcentaje_ahorro"],
                porcentaje_gasto_libre=e.validated_data["porcentaje_gasto_libre"],
                activo=e.validated_data.get("activo"),
                nombre=e.validated_data.get("nombre", "Mi plan"),
                fecha_inicio=e.validated_data.get("fecha_inicio"),
                fecha_fin=e.validated_data.get("fecha_fin"),
            )
        except PlanNoEncontrado as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_404_NOT_FOUND)
        except PorcentajesNoSuman100 as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(PlanFinancieroSerializer(plan).data, status=status.HTTP_200_OK)


class ActivarPlanView(APIView):
    """POST /api/planes-financieros/<plan_id>/activar/."""

    @extend_schema(
        tags=["Planes Financieros"],
        summary="Activar un plan financiero",
        description="Marca `plan_id` como el plan activo del usuario, desactivando el anterior si existía.",
        request=None,
        responses={
            200: PlanFinancieroSerializer,
            404: OpenApiResponse(description="No existe el plan."),
        },
    )
    def post(self, request: Request, plan_id: int) -> Response:
            caso = ActivarPlanFinancieroUseCase(repositorio=DjangoPlanFinancieroRepository())
            try:
                plan = caso.ejecutar(plan_id)
            except PlanNoEncontrado as ex:
                return Response({"detail": str(ex)}, status=status.HTTP_404_NOT_FOUND)
            return Response(PlanFinancieroSerializer(plan).data)



class ComparativaView(APIView):
    """GET: plan vs. ejecucion real de un periodo (?mes=&anio=)."""

    @extend_schema(
        tags=["Planes Financieros"],
        summary="Comparar plan activo vs. ejecución real",
        description="Metas del plan activo (gasto fijo/ahorro/gasto libre) vs. ingresos y gastos reales del periodo.",
        parameters=[
            OpenApiParameter("mes", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True, description="Mes del periodo (1-12)."),
            OpenApiParameter("anio", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True, description="Año del periodo."),
        ],
        responses={
            200: ComparativaPlanVsRealSerializer,
            404: OpenApiResponse(description="El usuario no tiene un plan activo."),
        },
    )
    def get(self, request: Request) -> Response:
            mes, anio = leer_periodo(request)
            caso = CompararPlanVsRealUseCase(
                plan_repositorio=DjangoPlanFinancieroRepository(),
                calcular_balance=CalcularBalanceMensualUseCase(
                    ingreso_repositorio=DjangoIngresoRepository(),
                    gasto_repositorio=DjangoGastoRepository(),
                ),
            )
            try:
                comp = caso.ejecutar(request.user.id, mes, anio)
            except PlanNoEncontrado as ex:
                return Response({"detail": str(ex)}, status=status.HTTP_404_NOT_FOUND)
            return Response(ComparativaPlanVsRealSerializer(comp).data)