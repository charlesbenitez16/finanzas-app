"""
Tests unitarios de las entidades de dominio: no requieren base de datos
ni Django corriendo, son Python puro. Correr con: uv run manage.py test
"""

from unittest import TestCase

from modules.catalogos.domain.entities import CategoriaGasto


class CategoriaGastoTests(TestCase):
    def test_es_global_cuando_no_tiene_usuario(self):
        categoria = CategoriaGasto(nombre="Vivienda", usuario_id=None)
        self.assertTrue(categoria.es_global())

    def test_no_es_global_cuando_tiene_usuario(self):
        categoria = CategoriaGasto(nombre="Mascotas", usuario_id=5)
        self.assertFalse(categoria.es_global())


class EntityBaseTests(TestCase):
    """Prueba el comportamiento heredado de shared/domain/base_entity.py."""

    def test_es_nueva_cuando_no_tiene_id(self):
        categoria = CategoriaGasto(nombre="Vivienda")
        self.assertTrue(categoria.es_nueva())

    def test_no_es_nueva_cuando_tiene_id(self):
        categoria = CategoriaGasto(id=1, nombre="Vivienda")
        self.assertFalse(categoria.es_nueva())
