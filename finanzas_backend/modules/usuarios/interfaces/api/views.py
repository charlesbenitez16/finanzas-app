"""
Vistas DRF del modulo usuarios: adaptadores primarios (driving).

Solo traducen HTTP <-> casos de uso: arman el caso de uso con su
repositorio, lo ejecutan con los datos del request y serializan la
respuesta. Sin logica de negocio, sin tocar el ORM. Mismo molde que
modules/catalogos/interfaces/api/views.py.

Emitir los JWT es responsabilidad de esta capa (interfaces/), no de los
casos de uso: los casos de uso siguen devolviendo el Usuario de dominio
"a secas"; acá se lo envuelve con el token para el front.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from modules.usuarios.application.use_cases.autenticar_usuario import (
    AutenticarUsuarioUseCase,
)
from modules.usuarios.application.use_cases.registrar_usuario import (
    RegistrarUsuarioUseCase,
)
from modules.usuarios.domain.entities import Usuario
from modules.usuarios.domain.exceptions import CredencialesInvalidas, EmailYaRegistrado
from modules.usuarios.infrastructure.repositories import DjangoUsuarioRepository
from modules.usuarios.interfaces.api.serializers import (
    LoginSerializer,
    RegistroUsuarioSerializer,
    TokenAuthSerializer,
    UsuarioSerializer,
)

AuthUser = get_user_model()


def _emitir_tokens(usuario: Usuario) -> dict:
    """
    Arma el par access/refresh para el auth.User vinculado a este
    Usuario de dominio. Requiere que DjangoUsuarioRepository.crear() ya
    haya seteado usuario.auth_user_id (siempre lo hace, para usuarios
    creados via /registro/).
    """
    auth_user = AuthUser.objects.get(id=usuario.auth_user_id)
    refresh = RefreshToken.for_user(auth_user)
    return {
        "usuario": UsuarioSerializer(usuario).data,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class RegistroView(APIView):
    """POST: alta de un usuario nuevo. Devuelve el usuario YA con tokens (auto-login)."""

    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Usuarios"],
        summary="Registrar un usuario nuevo",
        description=(
            "Alta de usuario (crea el perfil en `usuarios` y su auth.User "
            "vinculado). El email debe ser único; la contraseña se guarda "
            "hasheada. Devuelve el usuario ya autenticado (access + refresh), "
            "no hace falta llamar a /login/ después."
        ),
        request=RegistroUsuarioSerializer,
        responses={
            201: TokenAuthSerializer,
            400: OpenApiResponse(description="Ya existe un usuario con ese email."),
        },
    )
    def post(self, request: Request) -> Response:
        entrada = RegistroUsuarioSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        caso = RegistrarUsuarioUseCase(repositorio=DjangoUsuarioRepository(), hasher=make_password)

        try:
            usuario = caso.ejecutar(
                nombre=entrada.validated_data['nombre'],
                email=entrada.validated_data['email'],
                password_plano=entrada.validated_data['password']
            )
        except EmailYaRegistrado as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(_emitir_tokens(usuario), status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """POST: valida credenciales y devuelve el usuario + tokens JWT."""

    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Usuarios"],
        summary="Login",
        description=(
            "Valida email + contraseña. Si son correctos y el usuario está "
            "activo, devuelve el usuario + un par de tokens JWT: guardá "
            "`access` y mandalo como 'Authorization: Bearer <access>' en el "
            "resto de la API."
        ),
        request=LoginSerializer,
        responses={
            200: TokenAuthSerializer,
            401: OpenApiResponse(description="Email o contraseña incorrectos, o usuario inactivo."),
        },
    )
    def post(self, request: Request) -> Response:
        entrada = LoginSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        caso = AutenticarUsuarioUseCase(repositorio=DjangoUsuarioRepository(), verificador=check_password)

        try:
            usuario = caso.ejecutar(
                email=entrada.validated_data['email'],
                password_plano=entrada.validated_data['password']
            )
        except CredencialesInvalidas as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(_emitir_tokens(usuario))
