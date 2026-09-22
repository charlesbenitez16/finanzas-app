"""
Tests de integracion del repositorio Django ORM de planes_financieros.
Necesitan base de datos real: uv run manage.py test.

GOTCHA (ver modules/catalogos/tests/infrastructure/test_repositories.py):
PlanFinancieroModel es managed = False; Django NO crea la tabla en la
base de test. Se crea aca con SQL crudo en setUpClass (IF NOT EXISTS),
incluido el indice unico parcial uq_plan_activo_usuario para poder
probar la regla de "un solo plan activo".
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase

from modules.planes_financieros.domain.entities import PlanFinanciero
from modules.planes_financieros.infrastructure.repositories import (
    DjangoPlanFinancieroRepository,
)


class DjangoPlanFinancieroRepositoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS plan_financiero (
                    id BIGSERIAL PRIMARY KEY,
                    usuario_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
                    nombre VARCHAR(100) NOT NULL DEFAULT 'Mi plan',
                    porcentaje_gasto_fijo NUMERIC(5,2) NOT NULL,
                    porcentaje_ahorro NUMERIC(5,2) NOT NULL,
                    porcentaje_gasto_libre NUMERIC(5,2) NOT NULL,
                    fecha_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
                    fecha_fin DATE,
                    activo BOOLEAN NOT NULL DEFAULT TRUE
                )
                """
            )
            cursor.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS uq_plan_activo_usuario
                ON plan_financiero(usuario_id) WHERE activo = TRUE
                """
            )

    def setUp(self):
        self.repo = DjangoPlanFinancieroRepository()
        self.usuario = get_user_model().objects.create_user(
            username="tester", password="clave-de-prueba-123"
        )

    def test_crear_y_obtener_plan_activo(self):
        self.skipTest("TODO: implementar")

    def test_obtener_plan_activo_devuelve_none_si_no_hay(self):
        self.skipTest("TODO: implementar")
