"""
Tests de integracion del repositorio Django ORM de servicios_fijos.
Necesitan base de datos real: uv run manage.py test.

GOTCHA (ver modules/catalogos/tests/infrastructure/test_repositories.py):
ServicioFijoModel es managed = False; Django NO crea la tabla en la base
de test. Se crea aca con SQL crudo en setUpClass (IF NOT EXISTS). El DDL
es un subconjunto minimo del de 01_schema.sql. Las FK a categorias_gasto
/ niveles_prioridad tambien hacen falta: crealas antes (o simplifica el
DDL de test a columnas planas si no vas a probar la integridad referencial).
"""

from datetime import date

from django.db import connection
from django.test import TestCase

from modules.servicios_fijos.domain.entities import ServicioFijo
from modules.servicios_fijos.infrastructure.repositories import (
    DjangoServicioFijoRepository,
)


class DjangoServicioFijoRepositoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS servicios_fijos (
                    id BIGSERIAL PRIMARY KEY,
                    usuario_id INTEGER,
                    categoria_id INTEGER,
                    prioridad_id INTEGER,
                    nombre VARCHAR(150) NOT NULL,
                    dia_vencimiento SMALLINT NOT NULL,
                    monto_estimado NUMERIC(12,2),
                    es_monto_variable BOOLEAN NOT NULL DEFAULT FALSE,
                    dias_anticipacion_alerta SMALLINT NOT NULL DEFAULT 3,
                    activo BOOLEAN NOT NULL DEFAULT TRUE,
                    fecha_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
                    fecha_fin DATE,
                    notas TEXT
                )
                """
            )

    def setUp(self):
        self.repo = DjangoServicioFijoRepository()

    def test_crear_y_obtener_por_id(self):
        self.skipTest("TODO: implementar")

    def test_listar_por_usuario_solo_activos(self):
        self.skipTest("TODO: implementar")

    def test_listar_proximos_a_vencer(self):
        self.skipTest("TODO: implementar")
