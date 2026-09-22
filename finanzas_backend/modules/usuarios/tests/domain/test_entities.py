"""
Tests de la entidad Usuario. Python puro, sin Django ni base de datos.
Correr con: uv run manage.py test modules.usuarios
(o: uv run python -m unittest modules.usuarios.tests.domain.test_entities -v)
"""

from unittest import TestCase

from modules.usuarios.domain.entities import Usuario


class UsuarioTests(TestCase):
    def test_esta_activo_refleja_el_flag(self):
        # TODO: [crear Usuario(activo=True) y Usuario(activo=False);
        #        verificar esta_activo() en cada caso.]
        self.skipTest("TODO: implementar")

    def test_desactivar_pone_activo_en_false(self):
        # TODO: [crear Usuario activo, llamar desactivar(),
        #        assert not usuario.esta_activo().]
        self.skipTest("TODO: implementar")


class EntityBaseTests(TestCase):
    """Comportamiento heredado de shared/domain/base_entity.py."""

    def test_es_nueva_cuando_no_tiene_id(self):
        # TODO: [un Usuario sin id debe devolver es_nueva() == True.]
        self.skipTest("TODO: implementar")

    def test_no_es_nueva_cuando_tiene_id(self):
        # TODO: [Usuario(id=1, ...).es_nueva() == False.]
        self.skipTest("TODO: implementar")
