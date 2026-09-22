"""
Implementacion Django ORM de los puertos de domain/ports/repositories.py.

Traduce entre el mundo del ORM (UsuarioModel) y el del dominio (Usuario).
El metodo _a_entidad() es el corazon del patron (ver el mismo en
modules/catalogos/infrastructure/repositories.py).

Ademas, este repositorio es el unico lugar que sabe que un Usuario de
dominio esta respaldado por DOS filas: `usuarios` (perfil, este modulo) y
`auth_user` (credenciales reales de Django). crear()/actualizar() las
mantienen sincronizadas; el resto de la app (casos de uso, vistas) no
necesita saber que existen dos tablas.
"""

from typing import Optional

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

from modules.usuarios.domain.entities import Usuario
from modules.usuarios.domain.exceptions import EmailYaRegistrado
from modules.usuarios.domain.ports.repositories import UsuarioRepository
from modules.usuarios.infrastructure.models import UsuarioModel

AuthUser = get_user_model()


class DjangoUsuarioRepository(UsuarioRepository):
    def _a_entidad(self, modelo: UsuarioModel) -> Usuario:
        """
        CONSIGNA: construir un Usuario de dominio a partir de un
        UsuarioModel. Mapeo 1:1 por ahora.

        Retorno: Usuario
        """
        return Usuario(
            id=modelo.id,
            nombre=modelo.nombre,
            email=modelo.email,
            password_hash=modelo.password_hash,
            fecha_registro=modelo.fecha_registro,
            activo=modelo.activo,
            auth_user_id=modelo.auth_user_id,
        )

    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        try:
            user = UsuarioModel.objects.get(id=usuario_id)
            return self._a_entidad(user)
        except UsuarioModel.DoesNotExist:
            return None

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        user = UsuarioModel.objects.filter(email__iexact=email).first()
        return self._a_entidad(user) if user else None

    def existe_email(self, email: str) -> bool:
        return UsuarioModel.objects.filter(email__iexact=email).exists()

    def crear(self, usuario: Usuario) -> Usuario:
        """
        Crea el auth.User (lo que realmente autentica) y la fila
        `usuarios` (perfil) en una sola transaccion: si algo falla, no
        queda ninguna de las dos a medio crear.

        usuario.password_hash ya viene hasheado (lo calculo el caso de
        uso via el `hasher` inyectado). Se lo asignamos directo al
        auth.User (`password=...`) en vez de auth.User.objects.create_user(),
        para no hashear dos veces: las dos filas terminan con el MISMO
        hash.
        """
        try:
            with transaction.atomic():
                auth_user = AuthUser(
                    username=usuario.email,
                    email=usuario.email,
                    password=usuario.password_hash,
                    is_active=usuario.activo,
                )
                auth_user.save()

                modelo = UsuarioModel.objects.create(
                    nombre=usuario.nombre,
                    email=usuario.email,
                    password_hash=usuario.password_hash,
                    activo=usuario.activo,
                    auth_user_id=auth_user.id,
                )
        except IntegrityError as exc:
            raise EmailYaRegistrado(usuario.email) from exc
        return self._a_entidad(modelo)

    def actualizar(self, usuario: Usuario) -> Usuario:
        UsuarioModel.objects.filter(id=usuario.id).update(
            nombre=usuario.nombre,
            email=usuario.email,
            password_hash=usuario.password_hash,
            activo=usuario.activo,
        )
        # Sincronizar la baja/alta logica con el auth.User real: si no,
        # un usuario "desactivado" en `usuarios` seguiria pudiendo
        # autenticarse (sesion/Basic/JWT), porque eso lo controla
        # auth_user.is_active, no usuarios.activo.
        if usuario.auth_user_id is not None:
            AuthUser.objects.filter(id=usuario.auth_user_id).update(
                is_active=usuario.activo
            )
        return usuario
