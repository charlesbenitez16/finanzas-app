"""Caso de uso: alta de un usuario nuevo en el sistema."""

from dataclasses import dataclass
from typing import Callable

from modules.usuarios.domain.entities import Usuario
from modules.usuarios.domain.exceptions import EmailYaRegistrado
from modules.usuarios.domain.ports.repositories import UsuarioRepository


@dataclass
class RegistrarUsuarioUseCase:
    """
    CONSIGNA
    --------
    Registra un usuario nuevo. Reglas:
      1. El email no puede estar ya registrado (usuarios.email UNIQUE).
         Si lo esta, lanzar EmailYaRegistrado.
      2. La contrasena llega EN CLARO y se guarda HASHEADA. El dominio no
         conoce el algoritmo de hash: es un detalle de infraestructura.
         Decidi como inyectarlo (un callable `hasher`, un port aparte,
         django.contrib.auth.hashers.make_password, ...).
      3. Construir la entidad Usuario (sin id, activo=True) y persistirla
         con el repositorio, que la devuelve ya con id.

    Params de ejecutar():
        nombre: str
        email: str
        password_plano: str
    Retorno: Usuario (ya con id; es_nueva() == False)
    """

    repositorio: UsuarioRepository
    hasher: Callable[[str], str]

    def ejecutar(self, nombre: str, email: str, password_plano: str) -> Usuario:

      email = email.strip().lower()
      if self.repositorio.existe_email(email):
         raise EmailYaRegistrado(f"Ya existe un usuario con el email {email}")
      user = Usuario(
         nombre=nombre.strip(),
         email=email,
         password_hash=self.hasher(password_plano),
         activo=True
      )

      return self.repositorio.crear(user)
         
