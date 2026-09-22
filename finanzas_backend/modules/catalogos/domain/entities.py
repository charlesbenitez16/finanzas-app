"""
Entidades de dominio del modulo catalogos: CategoriaGasto y NivelPrioridad.

Son clases de Python puro (dataclasses), sin ningun import de Django.
Representan las mismas dos tablas que ya definimos en schema_finanzas.sql:
categorias_gasto y niveles_prioridad.
"""

from dataclasses import dataclass
from typing import Optional

from shared.domain.base_entity import Entity


@dataclass
class CategoriaGasto(Entity):
    """
    Categoria de gasto (ej. "Alimentacion", "Servicios Basicos").

    usuario_id en None significa categoria global del sistema; con valor,
    es una categoria personalizada creada por ese usuario.
    """

    nombre: str = ""
    icono: Optional[str] = None
    usuario_id: Optional[int] = None

    def es_global(self) -> bool:
        """True si es una categoria del catalogo global (no de un usuario)."""
        return self.usuario_id is None


@dataclass
class NivelPrioridad(Entity):
    """
    Nivel de prioridad de un gasto o servicio fijo (Esencial, Importante,
    Prescindible). Se usa en la simulacion de modo emergencia.
    """

    nombre: str = ""
    nivel_orden: int = 0
    descripcion: Optional[str] = None
    color: Optional[str] = None

    # DECISION DE DISENO (resuelta): la version anterior de este archivo
    # tenia un metodo es_prescindible() marcado como TODO, con una pista
    # para pensar si realmente le corresponde a esta entidad. La respuesta
    # es que NO: un NivelPrioridad aislado no conoce el resto de los
    # niveles que existen, asi que no puede decidir por si solo si es "el
    # mas bajo". Esa comparacion necesita ver TODOS los niveles a la vez,
    # asi que vive donde SI hay ese contexto completo: el futuro caso de
    # uso de modo emergencia (modulo gastos), que va a llamar a
    # NivelPrioridadRepository.listar_todos() y comparar nivel_orden entre
    # ellos (el mayor nivel_orden = el mas prescindible).
    #
    # Leccion para replicar en los proximos modulos: no toda propiedad que
    # "suena" a la entidad tiene que vivir en la entidad. Si necesita
    # conocer a sus hermanos para responder, probablemente pertenece a un
    # caso de uso o a un metodo del repositorio, no a la entidad.
