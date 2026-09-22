"""
Puertos del dominio de servicios_fijos. Los implementa
infrastructure/repositories.py con Django ORM.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from modules.servicios_fijos.domain.entities import ServicioFijo


class ServicioFijoRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, servicio_id: int) -> Optional[ServicioFijo]:
        """Devuelve el ServicioFijo con ese id, o None."""
        ...

    @abstractmethod
    def crear(self, servicio: ServicioFijo) -> ServicioFijo:
        """Persiste un ServicioFijo nuevo y lo devuelve con id."""
        ...

    @abstractmethod
    def actualizar(self, servicio: ServicioFijo) -> ServicioFijo:
        """Persiste cambios de un ServicioFijo existente (ej. baja logica)."""
        ...

    @abstractmethod
    def listar_por_usuario(
        self, usuario_id: int, solo_activos: bool = False
    ) -> list[ServicioFijo]:
        """
        Servicios fijos de un usuario. Si solo_activos=True, filtra
        activo = TRUE. Aprovecha idx_servicios_usuario (usuario_id).

        MAPEO SQL:
            SELECT * FROM servicios_fijos
            WHERE usuario_id = %s [AND activo = TRUE]
            ORDER BY nombre
        """
        ...

    @abstractmethod
    def listar_proximos_a_vencer(
        self, fecha_referencia: date
    ) -> list[ServicioFijo]:
        """
        MAPEO SQL -- query comentada al final de 01_schema.sql
        (generador de alertas / vista E). Traer los servicios activos
        cuyo vencimiento cae dentro de su ventana de anticipacion,
        parado en `fecha_referencia`:

            SELECT sf.*
            FROM servicios_fijos sf
            WHERE sf.activo = TRUE
              AND (sf.dia_vencimiento - EXTRACT(DAY FROM %(hoy)s)::int)
                    = sf.dias_anticipacion_alerta
            -- el "AND NOT EXISTS (pago de este mes)" lo resuelve el caso
            -- de uso del modulo alertas cruzando con GastoRepository.

        Retorno: list[ServicioFijo]
        """
        ...
