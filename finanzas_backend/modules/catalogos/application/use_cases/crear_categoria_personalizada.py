"""Caso de uso: un usuario crea su propia categoria de gasto."""

from dataclasses import dataclass
from typing import Optional

from modules.catalogos.domain.entities import CategoriaGasto
from modules.catalogos.domain.exceptions import NombreCategoriaDuplicado
from modules.catalogos.domain.ports.repositories import CategoriaGastoRepository


@dataclass
class CrearCategoriaPersonalizadaUseCase:
    repositorio: CategoriaGastoRepository

    def ejecutar(
        self, usuario_id: int, nombre: str, icono: Optional[str] = None
    ) -> CategoriaGasto:
        # 1. Regla de negocio: un usuario no puede tener dos categorias
        # PERSONALES con el mismo nombre (case-insensitive). No comparamos
        # contra las categorias globales: dos usuarios distintos pueden
        # crear "Mascotas" sin problema, y el UNIQUE (usuario_id, nombre)
        # de la base de datos ya modela exactamente esa regla.
        #
        # Nota: esto trae TODAS las categorias del usuario a memoria para
        # comparar. Para un catalogo chico (docenas de categorias por
        # usuario) es una simplificacion razonable; si esto creciera
        # mucho, convendria agregar un metodo dedicado al repositorio,
        # ej. existe_categoria_con_nombre(usuario_id, nombre).
        categorias_existentes = self.repositorio.listar_para_usuario(usuario_id)
        ya_existe = any(
            categoria.usuario_id == usuario_id
            and categoria.nombre.strip().lower() == nombre.strip().lower()
            for categoria in categorias_existentes
        )
        if ya_existe:
            raise NombreCategoriaDuplicado(
                f"Ya existe una categoria '{nombre}' para este usuario."
            )

        # 2. Crear la entidad de dominio (todavia sin id: es "nueva" en el
        # sentido de Entity.es_nueva()).
        categoria_nueva = CategoriaGasto(
            usuario_id=usuario_id, nombre=nombre.strip(), icono=icono
        )

        # 3. Persistirla. El repositorio devuelve la entidad ya con id
        # asignado por la base de datos.
        return self.repositorio.crear(categoria_nueva)
