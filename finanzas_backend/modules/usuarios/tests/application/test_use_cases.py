"""
Tests de los casos de uso de usuarios con un repositorio falso en
memoria (mismo contrato que DjangoUsuarioRepository, respaldado por una
lista de Python). Asi se prueba la logica de aplicacion sin base de
datos. Ver el ejemplo completo en
modules/catalogos/tests/application/test_use_cases.py.
"""

from unittest import TestCase

from modules.usuarios.domain.entities import Usuario
from modules.usuarios.domain.ports.repositories import UsuarioRepository


class RepositorioUsuarioFalso(UsuarioRepository):
    """Implementacion en memoria del puerto UsuarioRepository."""

    def __init__(self, usuarios_iniciales=None):
        self._usuarios = list(usuarios_iniciales or [])
        ids = [u.id for u in self._usuarios if u.id is not None]
        self._siguiente_id = max(ids, default=0) + 1

    def obtener_por_id(self, usuario_id):
        # TODO: [buscar en self._usuarios por id, o None.]
        raise NotImplementedError("Implementar el doble de test")

    def obtener_por_email(self, email):
        # TODO: [buscar por email case-insensitive, o None.]
        raise NotImplementedError("Implementar el doble de test")

    def existe_email(self, email):
        # TODO: [any(u.email.lower() == email.lower() for u in self._usuarios).]
        raise NotImplementedError("Implementar el doble de test")

    def crear(self, usuario):
        # TODO: [clonar con id=self._siguiente_id, append, incrementar,
        #        devolver la copia.]
        raise NotImplementedError("Implementar el doble de test")

    def actualizar(self, usuario):
        # TODO: [reemplazar en la lista el usuario con el mismo id.]
        raise NotImplementedError("Implementar el doble de test")


class RegistrarUsuarioUseCaseTests(TestCase):
    def test_registra_usuario_nuevo_con_id(self):
        self.skipTest("TODO: implementar")

    def test_email_duplicado_lanza_EmailYaRegistrado(self):
        self.skipTest("TODO: implementar")

    def test_password_se_guarda_hasheada_no_en_claro(self):
        self.skipTest("TODO: implementar")


class AutenticarUsuarioUseCaseTests(TestCase):
    def test_credenciales_validas_devuelven_el_usuario(self):
        self.skipTest("TODO: implementar")

    def test_usuario_inactivo_lanza_CredencialesInvalidas(self):
        self.skipTest("TODO: implementar")

    def test_password_incorrecta_lanza_CredencialesInvalidas(self):
        self.skipTest("TODO: implementar")
