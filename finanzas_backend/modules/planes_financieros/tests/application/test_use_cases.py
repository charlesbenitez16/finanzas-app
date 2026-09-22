"""
Tests de los casos de uso de planes_financieros con un repositorio falso
en memoria. Ver el patron en
modules/catalogos/tests/application/test_use_cases.py.
"""

from unittest import TestCase

from modules.planes_financieros.domain.entities import PlanFinanciero
from modules.planes_financieros.domain.ports.repositories import (
    PlanFinancieroRepository,
)


class RepositorioPlanFinancieroFalso(PlanFinancieroRepository):
    """Implementacion en memoria del puerto PlanFinancieroRepository."""

    def __init__(self, planes_iniciales=None):
        self._planes = list(planes_iniciales or [])
        ids = [p.id for p in self._planes if p.id is not None]
        self._siguiente_id = max(ids, default=0) + 1

    def obtener_por_id(self, plan_id):
        raise NotImplementedError("Implementar el doble de test")

    def crear(self, plan):
        raise NotImplementedError("Implementar el doble de test")

    def actualizar(self, plan):
        raise NotImplementedError("Implementar el doble de test")

    def listar_por_usuario(self, usuario_id):
        raise NotImplementedError("Implementar el doble de test")

    def obtener_plan_activo(self, usuario_id):
        raise NotImplementedError("Implementar el doble de test")


class CrearPlanFinancieroUseCaseTests(TestCase):
    def test_crea_plan_valido(self):
        self.skipTest("TODO: implementar")

    def test_porcentajes_que_no_suman_100_lanzan_PorcentajesNoSuman100(self):
        self.skipTest("TODO: implementar")


class ActivarPlanFinancieroUseCaseTests(TestCase):
    def test_activar_desactiva_el_plan_activo_anterior(self):
        self.skipTest("TODO: implementar")

    def test_plan_inexistente_lanza_PlanNoEncontrado(self):
        self.skipTest("TODO: implementar")


class CompararPlanVsRealUseCaseTests(TestCase):
    def test_sin_plan_activo_lanza_PlanNoEncontrado(self):
        self.skipTest("TODO: implementar")

    def test_metas_son_porcentajes_del_total_de_ingresos(self):
        self.skipTest("TODO: implementar")
