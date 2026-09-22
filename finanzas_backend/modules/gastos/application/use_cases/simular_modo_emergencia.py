"""Caso de uso: simulacion de "modo emergencia" (ahorro potencial por prioridad)."""

from dataclasses import dataclass

from modules.catalogos.domain.ports.repositories import NivelPrioridadRepository
from modules.gastos.domain.entities import AhorroPorPrioridad
from modules.gastos.domain.ports.repositories import GastoRepository
from decimal import Decimal
from modules.gastos.domain.entities import AhorroEmergencia


@dataclass
class SimularModoEmergenciaUseCase:
    """
    CONSIGNA
    --------
    Este es EL caso de uso que el modulo catalogos anticipo en el
    comentario de NivelPrioridad (domain/entities.py): "el futuro caso de
    uso de modo emergencia (modulo gastos) va a llamar a
    NivelPrioridadRepository.listar_todos() y comparar nivel_orden entre
    ellos (el mayor nivel_orden = el mas prescindible)".

    Reproduce vista_ahorro_potencial_por_prioridad y ademas calcula el
    ahorro ACUMULADO si el usuario fuera suspendiendo gastos de mas
    prescindible (mayor nivel_orden) hacia mas esencial:

      1. gastos_por_prioridad = self.gasto_repositorio.total_por_prioridad(
             usuario_id, periodo_mes, periodo_anio)  # ya viene por nivel_orden
      2. niveles = self.nivel_prioridad_repositorio.listar_todos()  # ordenados
      3. recorrer de mayor nivel_orden a menor, acumulando el ahorro:
         "si suspendo Prescindible ahorro X; si ademas suspendo Importante
         ahorro X + Y; ...". El nivel mas esencial (nivel_orden = 1)
         normalmente NO se suspende: decidi si lo incluis en el acumulado.

    Params de ejecutar(): usuario_id: int, periodo_mes: int, periodo_anio: int
    Retorno: a definir por vos. Sugerencia: una lista de dataclasses con
        (prioridad, nivel_orden, total_periodo, ahorro_acumulado_si_suspende).
        Podes reutilizar AhorroPorPrioridad y envolverlo, o crear un nuevo
        objeto de lectura en domain/entities.py.
    """

    gasto_repositorio: GastoRepository
    nivel_prioridad_repositorio: NivelPrioridadRepository

    def ejecutar(
        self, usuario_id: int, periodo_mes: int, periodo_anio: int
    ) -> list[AhorroPorPrioridad]:
        gastos = {
            fila.nivel_orden: fila.total_por_prioridad
            for fila in self.gasto_repositorio.total_por_prioridad(
                usuario_id, periodo_mes, periodo_anio)
        }
        niveles = {n.nivel_orden: n
                   for n in self.nivel_prioridad_repositorio.listar_todos()}

        acumulado = Decimal("0")
        filas = []
        # de MÁS prescindible (mayor nivel_orden) a MÁS esencial (1)
        for orden in sorted(niveles, reverse=True):
            total = gastos.get(orden, Decimal("0"))
            acumulado += total
            filas.append(AhorroEmergencia(
                prioridad=niveles[orden].nombre,
                nivel_orden=orden,
                total_periodo=total,
                ahorro_acumulado_si_suspende=acumulado,
            ))
        filas.reverse()                       # volver al orden natural (1..3)
        return filas
