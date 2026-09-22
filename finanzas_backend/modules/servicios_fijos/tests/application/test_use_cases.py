"""
Tests de los casos de uso de servicios_fijos con un repositorio falso en
memoria (mismo contrato que DjangoServicioFijoRepository). Ver el
ejemplo completo en modules/catalogos/tests/application/test_use_cases.py.
"""

from unittest import TestCase

from modules.servicios_fijos.domain.entities import ServicioFijo
from modules.servicios_fijos.domain.ports.repositories import ServicioFijoRepository


class RepositorioServicioFijoFalso(ServicioFijoRepository):
    """Implementacion en memoria del puerto ServicioFijoRepository."""

    def __init__(self, servicios_iniciales=None):
        self._servicios = list(servicios_iniciales or [])
        ids = [s.id for s in self._servicios if s.id is not None]
        self._siguiente_id = max(ids, default=0) + 1

    def obtener_por_id(self, servicio_id):
        raise NotImplementedError("Implementar el doble de test")

    def crear(self, servicio):
        raise NotImplementedError("Implementar el doble de test")

    def actualizar(self, servicio):
        raise NotImplementedError("Implementar el doble de test")

    def listar_por_usuario(self, usuario_id, solo_activos=False):
        raise NotImplementedError("Implementar el doble de test")

    def listar_proximos_a_vencer(self, fecha_referencia):
        raise NotImplementedError("Implementar el doble de test")


class CrearServicioFijoUseCaseTests(TestCase):
    def test_crea_servicio_con_id(self):
        self.skipTest("TODO: implementar")

    def test_dia_vencimiento_fuera_de_rango_lanza_DiaVencimientoInvalido(self):
        self.skipTest("TODO: implementar")

    def test_fecha_fin_anterior_a_inicio_lanza_RangoFechasInvalido(self):
        self.skipTest("TODO: implementar")


class ListarServiciosActivosUseCaseTests(TestCase):
    def test_devuelve_solo_los_activos(self):
        self.skipTest("TODO: implementar")


class ListarServiciosProximosAVencerUseCaseTests(TestCase):
    def test_usa_hoy_cuando_no_se_pasa_fecha(self):
        self.skipTest("TODO: implementar")
