"""
Tests de la entidad AlertaPago y su maquina de estados. Python puro, sin
Django ni base de datos.
"""

from unittest import TestCase

from modules.alertas.domain.entities import AlertaPago


class AlertaPagoTests(TestCase):
    def test_esta_pendiente_al_crearse(self):
        # TODO: [AlertaPago().esta_pendiente() == True (estado default).]
        self.skipTest("TODO: implementar")

    def test_marcar_enviada_desde_pendiente_ok(self):
        self.skipTest("TODO: implementar")

    def test_marcar_leida_sin_pasar_por_enviada_lanza_TransicionEstadoInvalida(self):
        self.skipTest("TODO: implementar")

    def test_resolver_setea_gasto_id_y_estado_resuelta(self):
        # TODO: [alerta.resolver(42) -> alerta.gasto_id == 42 y
        #        alerta.esta_resuelta() == True.]
        self.skipTest("TODO: implementar")
