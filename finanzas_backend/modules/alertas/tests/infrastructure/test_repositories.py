"""
Tests de integracion del repositorio Django ORM de alertas. Necesitan
base de datos real: uv run manage.py test.

GOTCHA (ver modules/catalogos/tests/infrastructure/test_repositories.py):
AlertaPagoModel es managed = False; Django NO crea la tabla en la base de
test. Se crea aca con SQL crudo en setUpClass (IF NOT EXISTS). El DDL de
test usa columnas planas para las FK; ajustalo si necesitas integridad
referencial. 01_schema.sql sigue siendo la fuente de verdad.
"""

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase

from modules.alertas.domain.entities import AlertaPago
from modules.alertas.infrastructure.repositories import DjangoAlertaPagoRepository


class DjangoAlertaPagoRepositoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS alertas_pago (
                    id BIGSERIAL PRIMARY KEY,
                    usuario_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
                    servicio_fijo_id BIGINT NOT NULL,
                    gasto_id BIGINT,
                    periodo_mes SMALLINT NOT NULL,
                    periodo_anio SMALLINT NOT NULL,
                    fecha_alerta DATE NOT NULL,
                    estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
                    mensaje TEXT,
                    fecha_creacion TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )
            cursor.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS uq_alerta_servicio_periodo
                ON alertas_pago(servicio_fijo_id, periodo_anio, periodo_mes)
                """
            )

    def setUp(self):
        self.repo = DjangoAlertaPagoRepository()
        self.usuario = get_user_model().objects.create_user(
            username="tester", password="clave-de-prueba-123"
        )

    def test_crear_y_obtener_por_servicio_y_periodo(self):
        self.skipTest("TODO: implementar")

    def test_existe_alerta_para_servicio_en_periodo(self):
        self.skipTest("TODO: implementar")

    def test_listar_por_usuario_y_estado(self):
        self.skipTest("TODO: implementar")
