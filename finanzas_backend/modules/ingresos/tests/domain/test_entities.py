"""
Tests de la entidad Ingreso. Python puro, sin Django ni base de datos.
"""

from decimal import Decimal
from unittest import TestCase

from modules.ingresos.domain.entities import Ingreso


class IngresoTests(TestCase):
    def test_pertenece_al_periodo_true_para_su_mes_y_anio(self):
        # TODO: [Ingreso(periodo_mes=3, periodo_anio=2026)
        #        .pertenece_al_periodo(3, 2026) == True.]
        
        self.skipTest("TODO: implementar")

    def test_pertenece_al_periodo_false_para_otro_mes(self):
        self.skipTest("TODO: implementar")

    def test_es_monto_valido_false_para_monto_cero_o_negativo(self):
        # TODO: [Ingreso(monto=Decimal("0")).es_monto_valido() == False.]
        self.skipTest("TODO: implementar")
