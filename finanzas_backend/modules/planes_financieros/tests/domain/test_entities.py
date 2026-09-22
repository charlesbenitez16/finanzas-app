"""
Tests de la entidad PlanFinanciero. Python puro, sin Django ni base de datos.
"""

from decimal import Decimal
from unittest import TestCase

from modules.planes_financieros.domain.entities import PlanFinanciero


class PlanFinancieroTests(TestCase):
    def test_porcentajes_suman_100_true_para_50_20_30(self):
        # TODO: [PlanFinanciero(porcentaje_gasto_fijo=50, porcentaje_ahorro=20,
        #        porcentaje_gasto_libre=30).porcentajes_suman_100() == True.]
        self.skipTest("TODO: implementar")

    def test_porcentajes_suman_100_false_si_no_dan_100(self):
        self.skipTest("TODO: implementar")

    def test_meta_gasto_fijo_es_porcentaje_del_ingreso(self):
        # TODO: [con 50% y ingreso 800000 -> 400000.00.]
        self.skipTest("TODO: implementar")

    def test_esta_vigente_dentro_de_la_ventana(self):
        self.skipTest("TODO: implementar")
