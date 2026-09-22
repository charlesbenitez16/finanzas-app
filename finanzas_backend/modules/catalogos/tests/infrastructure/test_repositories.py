"""
Tests de integracion de los repositorios Django ORM. Estos SI necesitan
una base de datos real: Django crea y destruye una base de datos de test
automaticamente al correr: uv run manage.py test

GOTCHA importante: como CategoriaGastoModel y NivelPrioridadModel son
managed=False (ver infrastructure/models.py), Django NO crea esas tablas
en la base de datos de test -- a diferencia de auth_user, django_session,
etc., que si gestiona. Sin esto, estos tests fallarian con "relation
categorias_gasto does not exist".

La solucion: cada clase de test crea sus propias tablas con SQL crudo en
setUpClass (con IF NOT EXISTS, para que correr ambas clases en la misma
base de test no choque). El DDL es un subconjunto minimo del de
01_schema.sql -- ese script SQL sigue siendo la fuente de verdad real;
esto es solo un accesorio para que la base de test tenga donde escribir.

Nota: usuario_id referencia auth_user (la tabla que Django SI crea en la
base de test), no la tabla `usuarios` original del schema SQL -- 
coherente con el gotcha ya documentado en infrastructure/models.py sobre
AUTH_USER_MODEL.
"""

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase

from modules.catalogos.domain.entities import CategoriaGasto
from modules.catalogos.infrastructure.models import NivelPrioridadModel
from modules.catalogos.infrastructure.repositories import (
    DjangoCategoriaGastoRepository,
    DjangoNivelPrioridadRepository,
)


class DjangoCategoriaGastoRepositoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS categorias_gasto (
                    id SERIAL PRIMARY KEY,
                    usuario_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
                    nombre VARCHAR(100) NOT NULL,
                    icono VARCHAR(50),
                    UNIQUE (usuario_id, nombre)
                )
                """
            )

    def setUp(self):
        self.repo = DjangoCategoriaGastoRepository()
        self.usuario = get_user_model().objects.create_user(
            username="tester", password="clave-de-prueba-123"
        )

    def test_crear_y_obtener_categoria(self):
        categoria = self.repo.crear(
            CategoriaGasto(nombre="Mascotas", usuario_id=self.usuario.id)
        )

        self.assertFalse(categoria.es_nueva())

        encontrada = self.repo.obtener_por_id(categoria.id)
        self.assertIsNotNone(encontrada)
        self.assertEqual(encontrada.nombre, "Mascotas")
        self.assertEqual(encontrada.usuario_id, self.usuario.id)

    def test_obtener_por_id_inexistente_devuelve_none(self):
        self.assertIsNone(self.repo.obtener_por_id(999999))

    def test_listar_para_usuario_incluye_propias_y_globales(self):
        self.repo.crear(CategoriaGasto(nombre="Global de prueba", usuario_id=None))
        self.repo.crear(CategoriaGasto(nombre="Mascotas", usuario_id=self.usuario.id))

        resultado = self.repo.listar_para_usuario(self.usuario.id)
        nombres = {c.nombre for c in resultado}

        self.assertEqual(nombres, {"Global de prueba", "Mascotas"})


class DjangoNivelPrioridadRepositoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS niveles_prioridad (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(50) NOT NULL UNIQUE,
                    nivel_orden SMALLINT NOT NULL UNIQUE,
                    descripcion TEXT,
                    color VARCHAR(20)
                )
                """
            )

    def setUp(self):
        self.repo = DjangoNivelPrioridadRepository()

    def test_listar_todos_ordena_por_nivel_orden(self):
        NivelPrioridadModel.objects.create(nombre="Prescindible", nivel_orden=3)
        NivelPrioridadModel.objects.create(nombre="Esencial", nivel_orden=1)
        NivelPrioridadModel.objects.create(nombre="Importante", nivel_orden=2)

        resultado = self.repo.listar_todos()

        self.assertEqual(
            [nivel.nombre for nivel in resultado],
            ["Esencial", "Importante", "Prescindible"],
        )
