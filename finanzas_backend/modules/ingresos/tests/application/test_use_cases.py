"""
Tests de los casos de uso de ingresos con un repositorio falso en
memoria (mismo contrato que DjangoIngresoRepository). Ver el ejemplo
completo en modules/catalogos/tests/application/test_use_cases.py.
"""

from decimal import Decimal
from unittest import TestCase

from modules.ingresos.domain.entities import Ingreso
from modules.ingresos.domain.ports.repositories import IngresoRepository


class RepositorioIngresoFalso(IngresoRepository):
    """Implementacion en memoria del puerto IngresoRepository."""

    def __init__(self, ingresos_iniciales=None):
        self._ingresos = list(ingresos_iniciales or [])
        ids = [i.id for i in self._ingresos if i.id is not None]
        self._siguiente_id = max(ids, default=0) + 1

    def obtener_por_id(self, ingreso_id):
        # TODO: [buscar por id, o None.]
        raise NotImplementedError("Implementar el doble de test")

    def crear(self, ingreso):
        # TODO: [clonar con id=self._siguiente_id, append, incrementar.]
        raise NotImplementedError("Implementar el doble de test")

    def listar_por_usuario_y_periodo(self, usuario_id, periodo_mes, periodo_anio):
        # TODO: [filtrar self._ingresos por usuario y periodo.]
        raise NotImplementedError("Implementar el doble de test")

    def sumar_montos_por_periodo(self, usuario_id, periodo_mes, periodo_anio):
        # TODO: [sum(...) sobre los ingresos del periodo, Decimal("0") si
        #        no hay.]
        raise NotImplementedError("Implementar el doble de test")


class RegistrarIngresoUseCaseTests(TestCase):
    def test_crea_ingreso_con_id(self):
        self.skipTest("TODO: implementar")

    def test_monto_no_positivo_lanza_MontoInvalido(self):
        self.skipTest("TODO: implementar")

    def test_mes_fuera_de_rango_lanza_PeriodoInvalido(self):
        self.skipTest("TODO: implementar")


class CalcularTotalIngresosPeriodoUseCaseTests(TestCase):
    def test_suma_solo_los_ingresos_del_periodo_pedido(self):
        self.skipTest("TODO: implementar")

    def test_devuelve_cero_si_no_hay_ingresos(self):
        self.skipTest("TODO: implementar")
