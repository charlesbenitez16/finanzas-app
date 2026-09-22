"""
Tests de integracion del repositorio Django ORM de gastos. Necesitan
base de datos real: uv run manage.py test.

GOTCHA (ver modules/catalogos/tests/infrastructure/test_repositories.py):
GastoModel es managed = False; Django NO crea la tabla en la base de
test. Se crea aca con SQL crudo en setUpClass (IF NOT EXISTS). El DDL de
test usa columnas planas para las FK (sin REFERENCES) para no arrastrar
todo el resto del schema; ajustalo si necesitas probar integridad
referencial. 01_schema.sql sigue siendo la fuente de verdad.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase

from modules.gastos.domain.entities import Gasto
from modules.gastos.infrastructure.repositories import DjangoGastoRepository


class DjangoGastoRepositoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS gastos (
                    id BIGSERIAL PRIMARY KEY,
                    usuario_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
                    categoria_id INTEGER,
                    servicio_fijo_id BIGINT,
                    prioridad_id INTEGER,
                    monto NUMERIC(12,2) NOT NULL,
                    fecha_gasto DATE NOT NULL,
                    periodo_mes SMALLINT NOT NULL,
                    periodo_anio SMALLINT NOT NULL,
                    estado VARCHAR(20) NOT NULL DEFAULT 'Pagado',
                    descripcion TEXT,
                    fecha_registro TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )

    def setUp(self):
        self.repo = DjangoGastoRepository()
        self.usuario = get_user_model().objects.create_user(
            username="tester", password="clave-de-prueba-123"
        )

    def test_crear_y_obtener_por_id(self):
        self.skipTest("TODO: implementar")

    def test_existe_pago_de_servicio_en_periodo(self):
        self.skipTest("TODO: implementar")

    def test_sumar_montos_por_periodo(self):
        self.skipTest("TODO: implementar")

    def test_total_por_prioridad_agrupa_y_ordena_por_nivel_orden(self):
        self.skipTest("TODO: implementar")
