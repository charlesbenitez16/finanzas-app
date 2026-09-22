"""
Tests de integracion del repositorio Django ORM de usuarios. Necesitan
una base de datos real: uv run manage.py test.

GOTCHA (ver modules/catalogos/tests/infrastructure/test_repositories.py):
UsuarioModel es managed = False, asi que Django NO crea la tabla
`usuarios` en la base de test. Cada clase la crea con SQL crudo en
setUpClass (con IF NOT EXISTS). El DDL es un subconjunto minimo del de
01_schema.sql, que sigue siendo la fuente de verdad real.
"""

from django.db import connection
from django.test import TestCase

from modules.usuarios.domain.entities import Usuario
from modules.usuarios.infrastructure.repositories import DjangoUsuarioRepository


class DjangoUsuarioRepositoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id BIGSERIAL PRIMARY KEY,
                    nombre VARCHAR(150) NOT NULL,
                    email VARCHAR(150) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    fecha_registro TIMESTAMP NOT NULL DEFAULT NOW(),
                    activo BOOLEAN NOT NULL DEFAULT TRUE
                )
                """
            )

    def setUp(self):
        self.repo = DjangoUsuarioRepository()

    def test_crear_y_obtener_por_email(self):
        self.skipTest("TODO: implementar")

    def test_existe_email_es_case_insensitive(self):
        self.skipTest("TODO: implementar")

    def test_obtener_por_id_inexistente_devuelve_none(self):
        self.skipTest("TODO: implementar")
