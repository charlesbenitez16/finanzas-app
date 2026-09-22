"""
Tests de la entidad ServicioFijo. Python puro, sin Django ni base de datos.
"""

from datetime import date
from unittest import TestCase

from modules.servicios_fijos.domain.entities import ServicioFijo


class ServicioFijoTests(TestCase):
    def test_esta_activo_refleja_el_flag(self):
        self.skipTest("TODO: implementar")

    def test_esta_vigente_false_fuera_de_la_ventana_de_fechas(self):
        # TODO: [ServicioFijo(activo=True, fecha_inicio=date(2026,1,1),
        #        fecha_fin=date(2026,6,30)).esta_vigente(date(2026,8,1)) == False.]
        self.skipTest("TODO: implementar")

    def test_dias_para_vencimiento_cuenta_bien(self):
        self.skipTest("TODO: implementar")

    def test_debe_generar_alerta_true_a_los_dias_de_anticipacion_exactos(self):
        # TODO: [dia_vencimiento y dias_anticipacion_alerta tales que,
        #        parado en fecha_ref, falten exactamente esos dias.]
        self.skipTest("TODO: implementar")
