"""
Tests de los casos de uso de gastos con dobles en memoria de los puertos.

RepositorioGastoFalso implementa GastoRepository con una lista. Para
CalcularBalanceMensualUseCase tambien hace falta un doble de
IngresoRepository (o reutilizar RepositorioIngresoFalso de
modules/ingresos/tests). Para SimularModoEmergenciaUseCase, un doble de
NivelPrioridadRepository (o el de modules/catalogos/tests).
Ver el patron en modules/catalogos/tests/application/test_use_cases.py.
"""

from decimal import Decimal
from unittest import TestCase

from modules.gastos.domain.entities import AhorroPorPrioridad, Gasto
from modules.gastos.domain.ports.repositories import GastoRepository


class RepositorioGastoFalso(GastoRepository):
    """Implementacion en memoria del puerto GastoRepository."""

    def __init__(self, gastos_iniciales=None):
        self._gastos = list(gastos_iniciales or [])
        ids = [g.id for g in self._gastos if g.id is not None]
        self._siguiente_id = max(ids, default=0) + 1

    def obtener_por_id(self, gasto_id):
        raise NotImplementedError("Implementar el doble de test")

    def crear(self, gasto):
        raise NotImplementedError("Implementar el doble de test")

    def listar_por_usuario_y_periodo(self, usuario_id, periodo_mes, periodo_anio):
        raise NotImplementedError("Implementar el doble de test")

    def sumar_montos_por_periodo(self, usuario_id, periodo_mes, periodo_anio):
        raise NotImplementedError("Implementar el doble de test")

    def existe_pago_de_servicio_en_periodo(
        self, servicio_fijo_id, periodo_mes, periodo_anio
    ):
        raise NotImplementedError("Implementar el doble de test")

    def listar_pagos_de_servicio_fijo(self, servicio_fijo_id):
        raise NotImplementedError("Implementar el doble de test")

    def total_por_prioridad(self, usuario_id, periodo_mes, periodo_anio):
        raise NotImplementedError("Implementar el doble de test")


class RegistrarGastoUseCaseTests(TestCase):
    def test_crea_gasto_puntual_con_id_y_servicio_fijo_none(self):
        self.skipTest("TODO: implementar")

    def test_monto_no_positivo_lanza_MontoInvalido(self):
        self.skipTest("TODO: implementar")

    def test_publica_evento_GastoRegistrado(self):
        self.skipTest("TODO: implementar")


class RegistrarPagoDeServicioFijoUseCaseTests(TestCase):
    def test_pago_duplicado_en_el_periodo_lanza_PagoDeServicioDuplicado(self):
        self.skipTest("TODO: implementar")

    def test_crea_el_gasto_con_servicio_fijo_id_seteado(self):
        self.skipTest("TODO: implementar")


class CalcularBalanceMensualUseCaseTests(TestCase):
    def test_balance_es_ingresos_menos_gastos(self):
        self.skipTest("TODO: implementar")


class CalcularVariacionServiciosUseCaseTests(TestCase):
    def test_primer_periodo_tiene_variacion_none(self):
        self.skipTest("TODO: implementar")

    def test_calcula_porcentaje_respecto_al_mes_anterior(self):
        # TODO: [Agua 5000 -> 5500 => +10.00 (ejemplo del comentario de
        #        vista_variacion_servicios en 01_schema.sql).]
        self.skipTest("TODO: implementar")


class SimularModoEmergenciaUseCaseTests(TestCase):
    def test_acumula_ahorro_de_mas_prescindible_a_mas_esencial(self):
        self.skipTest("TODO: implementar")
