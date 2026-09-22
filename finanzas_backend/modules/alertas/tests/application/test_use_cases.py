"""
Tests de los casos de uso de alertas con dobles en memoria de los
puertos. Para GenerarAlertasDeVencimientoUseCase hace falta ademas un
doble de ServicioFijoRepository (o reusar RepositorioServicioFijoFalso de
modules/servicios_fijos/tests). Ver el patron en
modules/catalogos/tests/application/test_use_cases.py.
"""

from unittest import TestCase

from modules.alertas.domain.entities import AlertaPago
from modules.alertas.domain.ports.repositories import AlertaPagoRepository


class RepositorioAlertaPagoFalso(AlertaPagoRepository):
    """Implementacion en memoria del puerto AlertaPagoRepository."""

    def __init__(self, alertas_iniciales=None):
        self._alertas = list(alertas_iniciales or [])
        ids = [a.id for a in self._alertas if a.id is not None]
        self._siguiente_id = max(ids, default=0) + 1

    def obtener_por_id(self, alerta_id):
        raise NotImplementedError("Implementar el doble de test")

    def crear(self, alerta):
        raise NotImplementedError("Implementar el doble de test")

    def actualizar(self, alerta):
        raise NotImplementedError("Implementar el doble de test")

    def listar_por_usuario_y_estado(self, usuario_id, estado):
        raise NotImplementedError("Implementar el doble de test")

    def existe_alerta_para_servicio_en_periodo(
        self, servicio_fijo_id, periodo_mes, periodo_anio
    ):
        raise NotImplementedError("Implementar el doble de test")

    def obtener_por_servicio_y_periodo(
        self, servicio_fijo_id, periodo_mes, periodo_anio
    ):
        raise NotImplementedError("Implementar el doble de test")


class GenerarAlertasDeVencimientoUseCaseTests(TestCase):
    def test_crea_una_alerta_por_servicio_proximo_a_vencer(self):
        self.skipTest("TODO: implementar")

    def test_no_duplica_si_ya_existe_alerta_para_ese_servicio_y_periodo(self):
        self.skipTest("TODO: implementar")


class ListarAlertasPendientesUseCaseTests(TestCase):
    def test_devuelve_solo_las_del_estado_pedido(self):
        self.skipTest("TODO: implementar")


class MarcarAlertaUseCasesTests(TestCase):
    def test_marcar_enviada_persiste_la_transicion(self):
        self.skipTest("TODO: implementar")

    def test_alerta_inexistente_lanza_AlertaNoEncontrada(self):
        self.skipTest("TODO: implementar")


class ResolverAlertaAlPagarUseCaseTests(TestCase):
    def test_resuelve_la_alerta_del_servicio_y_periodo_del_evento(self):
        self.skipTest("TODO: implementar")

    def test_evento_sin_servicio_fijo_id_no_hace_nada(self):
        self.skipTest("TODO: implementar")
