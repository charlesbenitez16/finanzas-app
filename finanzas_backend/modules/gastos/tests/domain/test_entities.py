"""
Tests de la entidad Gasto. Python puro, sin Django ni base de datos.
"""

from decimal import Decimal
from unittest import TestCase

from modules.gastos.domain.entities import Gasto


class GastoTests(TestCase):
    def test_es_pago_de_servicio_fijo_segun_servicio_fijo_id(self):
        # TODO: [Gasto(servicio_fijo_id=5) -> True; Gasto(servicio_fijo_id=None) -> False.]
        self.skipTest("TODO: implementar")

    def test_esta_pagado_solo_con_estado_Pagado(self):
        self.skipTest("TODO: implementar")

    def test_pertenece_al_periodo(self):
        self.skipTest("TODO: implementar")

    def test_es_estado_valido_rechaza_estados_fuera_del_CHECK(self):
        # TODO: [Gasto(estado="Cualquiera").es_estado_valido() == False.]
        self.skipTest("TODO: implementar")
