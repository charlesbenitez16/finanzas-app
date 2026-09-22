"""Caso de uso: verificar email + contrasena y devolver el usuario."""

from dataclasses import dataclass
from typing import Callable

from modules.usuarios.domain.entities import Usuario
from modules.usuarios.domain.exceptions import CredencialesInvalidas
from modules.usuarios.domain.ports.repositories import UsuarioRepository


@dataclass
class AutenticarUsuarioUseCase:
    """
    CONSIGNA
    --------
    Dado un email y una contrasena en claro, devolver el Usuario si:
      - existe un usuario con ese email, Y
      - esta activo (usuario.esta_activo()), Y
      - el hash de la contrasena coincide con usuario.password_hash.
    En cualquier otro caso lanzar CredencialesInvalidas. Usa el MISMO
    error para "no existe" y "clave mala": no filtres cual de los dos fallo.

    La verificacion del hash es un detalle de infraestructura (igual que
    en RegistrarUsuarioUseCase): inyectalo como te resulte mas comodo.

    Params de ejecutar():
        email: str
        password_plano: str
    Retorno: Usuario
    """

    repositorio: UsuarioRepository
    verificador: Callable[[str, str], bool] 

    def ejecutar(self, email: str, password_plano: str) -> Usuario:
        email = email.strip().lower()
        user = self.repositorio.obtener_por_email(email)

        if user is None or not user.esta_activo():
            raise CredencialesInvalidas("Credenciales Invalidas")

        if not self.verificador(password_plano, user.password_hash):
            raise CredencialesInvalidas("Clave Invalida")

        return user

