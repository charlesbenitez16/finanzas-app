"""
Implementacion Django ORM de los puertos definidos en
domain/ports/repositories.py.

Esta es la pieza que traduce entre el mundo del ORM (los *Model) y el
mundo del dominio (las entidades CategoriaGasto / NivelPrioridad). Aca es
donde mas se nota la arquitectura hexagonal: si el dia de manana cambias
de base de datos, solo reescribis este archivo, nada mas.
"""

from typing import Optional

from django.db.models import Q

from modules.catalogos.domain.entities import CategoriaGasto, NivelPrioridad
from modules.catalogos.domain.ports.repositories import (
    CategoriaGastoRepository,
    NivelPrioridadRepository,
)
from modules.catalogos.infrastructure.models import CategoriaGastoModel, NivelPrioridadModel


class DjangoCategoriaGastoRepository(CategoriaGastoRepository):
    def _a_entidad(self, modelo: CategoriaGastoModel) -> CategoriaGasto:
        # El mapeo es 1 a 1 porque el modelo y la entidad tienen los
        # mismos campos, pero en un modulo con mas reglas de negocio este
        # metodo es donde traducirias tipos, calcularias campos derivados,
        # etc. Ojo: modelo.usuario_id (no modelo.usuario) para no
        # disparar una consulta extra a la base de datos trayendo el
        # objeto User completo cuando solo necesitamos el id.
        return CategoriaGasto(
            id=modelo.id,
            nombre=modelo.nombre,
            icono=modelo.icono,
            usuario_id=modelo.usuario_id,
        )

    def obtener_por_id(self, categoria_id: int) -> Optional[CategoriaGasto]:
        try:
            modelo = CategoriaGastoModel.objects.get(id=categoria_id)
        except CategoriaGastoModel.DoesNotExist:
            return None
        return self._a_entidad(modelo)

    def listar_para_usuario(self, usuario_id: int) -> list[CategoriaGasto]:
        # Q(usuario_id__isnull=True) = categorias globales
        # | Q(usuario_id=usuario_id) = las personalizadas de este usuario
        queryset = CategoriaGastoModel.objects.filter(
            Q(usuario_id__isnull=True) | Q(usuario_id=usuario_id)
        ).order_by("nombre")
        return [self._a_entidad(modelo) for modelo in queryset]

    def crear(self, categoria: CategoriaGasto) -> CategoriaGasto:
        modelo = CategoriaGastoModel.objects.create(
            usuario_id=categoria.usuario_id,
            nombre=categoria.nombre,
            icono=categoria.icono,
        )
        return self._a_entidad(modelo)


class DjangoNivelPrioridadRepository(NivelPrioridadRepository):
    def _a_entidad(self, modelo: NivelPrioridadModel) -> NivelPrioridad:
        return NivelPrioridad(
            id=modelo.id,
            nombre=modelo.nombre,
            nivel_orden=modelo.nivel_orden,
            descripcion=modelo.descripcion,
            color=modelo.color,
        )

    def obtener_por_id(self, nivel_id: int) -> Optional[NivelPrioridad]:
        try:
            modelo = NivelPrioridadModel.objects.get(id=nivel_id)
        except NivelPrioridadModel.DoesNotExist:
            return None
        return self._a_entidad(modelo)

    def listar_todos(self) -> list[NivelPrioridad]:
        queryset = NivelPrioridadModel.objects.order_by("nivel_orden")
        return [self._a_entidad(modelo) for modelo in queryset]
