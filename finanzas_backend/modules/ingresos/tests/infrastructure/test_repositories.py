"""
Tests de integracion del repositorio Django ORM de ingresos. Necesitan
base de datos real: uv run manage.py test.

GOTCHA (ver modules/catalogos/tests/infrastructure/test_repositories.py):
IngresoModel es managed = False, asi que Django NO crea la tabla
`ingresos` en la base de test. Se crea aca con SQL crudo en setUpClass
(IF NOT EXISTS). usuario_id referencia auth_user (la tabla que Django SI
crea en la base de test), coherente con el gotcha de AUTH_USER_MODEL.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase

from modules.ingresos.domain.entities import Ingreso
from modules.ingresos.infrastructure.repositories import DjangoIngresoRepository


class DjangoIngresoRepositoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ingresos (
                    id BIGSERIAL PRIMARY KEY,
                    usuario_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
                    monto NUMERIC(12,2) NOT NULL,
                    fecha DATE NOT NULL,
                    periodo_mes SMALLINT NOT NULL,
                    periodo_anio SMALLINT NOT NULL,
                    fuente VARCHAR(100),
                    descripcion TEXT,
                    fecha_registro TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )

    def setUp(self):
        self.repo = DjangoIngresoRepository()
        self.usuario = get_user_model().objects.create_user(
            username="tester", password="clave-de-prueba-123"
        )

    def test_crear_y_obtener_por_id(self):
        self.skipTest("TODO: implementar")

    def test_listar_por_usuario_y_periodo_filtra_bien(self):
        self.skipTest("TODO: implementar")

    def test_sumar_montos_por_periodo(self):
        self.skipTest("TODO: implementar")
