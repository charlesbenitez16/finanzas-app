"""
Vistas DRF del modulo catalogos: adaptadores primarios (driving).

Su unica responsabilidad es traducir HTTP <-> casos de uso. No contienen
logica de negocio ni acceden a los modelos Django directamente: eso vive
en application/ e infrastructure/ respectivamente. El patron se repite
igual en las tres vistas: 1) armar el caso de uso con su repositorio,
2) ejecutarlo con los datos del request, 3) serializar la respuesta.
"""

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.catalogos.application.use_cases.crear_categoria_personalizada import (
    CrearCategoriaPersonalizadaUseCase,
)
from modules.catalogos.application.use_cases.listar_categorias import ListarCategoriasUseCase
from modules.catalogos.application.use_cases.listar_niveles_prioridad import (
    ListarNivelesPrioridadUseCase,
)
from modules.catalogos.domain.exceptions import NombreCategoriaDuplicado
from modules.catalogos.infrastructure.repositories import (
    DjangoCategoriaGastoRepository,
    DjangoNivelPrioridadRepository,
)
from modules.catalogos.interfaces.api.serializers import (
    CategoriaGastoSerializer,
    NivelPrioridadSerializer,
)


class CategoriasGastoView(APIView):
    """GET: lista categorias del usuario autenticado. POST: crea una nueva."""

    # Requiere login porque una categoria personalizada siempre pertenece
    # a un usuario concreto (request.user.id). Sin el modulo usuarios
    # armado todavia, para probar esto a mano: uv run manage.py
    # createsuperuser, despues iniciar sesion en /admin/ y navegar a este
    # endpoint en el mismo navegador (la API navegable de DRF reutiliza
    # esa sesion).
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Catálogos"],
        summary="Listar categorías de gasto",
        description="Categorías globales del sistema (usuario_id nulo) + las personalizadas del usuario autenticado.",
        responses=CategoriaGastoSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        caso_de_uso = ListarCategoriasUseCase(repositorio=DjangoCategoriaGastoRepository())
        categorias = caso_de_uso.ejecutar(usuario_id=request.user.id)
        serializer = CategoriaGastoSerializer(categorias, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["Catálogos"],
        summary="Crear categoría personalizada",
        description="Crea una categoría de gasto propia del usuario autenticado.",
        request=CategoriaGastoSerializer,
        responses={
            201: CategoriaGastoSerializer,
            400: OpenApiResponse(description="Ya existe una categoría con ese nombre para este usuario."),
        },
    )
    def post(self, request: Request) -> Response:
        caso_de_uso = CrearCategoriaPersonalizadaUseCase(
            repositorio=DjangoCategoriaGastoRepository()
        )
        try:
            categoria = caso_de_uso.ejecutar(
                usuario_id=request.user.id,
                nombre=request.data.get("nombre", ""),
                icono=request.data.get("icono"),
            )
        except NombreCategoriaDuplicado as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CategoriaGastoSerializer(categoria)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NivelesPrioridadView(APIView):
    """GET: lista los niveles de prioridad disponibles (catalogo fijo, de lectura)."""

    @extend_schema(
        tags=["Catálogos"],
        summary="Listar niveles de prioridad",
        description="Catálogo fijo de solo lectura (Esencial, Importante, Prescindible), ordenado por nivel_orden.",
        responses=NivelPrioridadSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        caso_de_uso = ListarNivelesPrioridadUseCase(
            repositorio=DjangoNivelPrioridadRepository()
        )
        niveles = caso_de_uso.ejecutar()
        serializer = NivelPrioridadSerializer(niveles, many=True)
        return Response(serializer.data)
