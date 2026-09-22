"""
Tests de los casos de uso usando un repositorio falso en memoria en vez
de Django ORM. Esto es justamente lo que gana la arquitectura hexagonal:
podes probar toda la logica de aplicacion sin tocar la base de datos.
"""

from unittest import TestCase

from modules.catalogos.application.use_cases.crear_categoria_personalizada import (
    CrearCategoriaPersonalizadaUseCase,
)
from modules.catalogos.application.use_cases.listar_categorias import ListarCategoriasUseCase
from modules.catalogos.domain.entities import CategoriaGasto
from modules.catalogos.domain.exceptions import NombreCategoriaDuplicado


class RepositorioCategoriaGastoFalso:
    """
    Implementacion en memoria del puerto CategoriaGastoRepository (mismo
    contrato que domain/ports/repositories.py define, pero respaldada por
    una lista de Python en vez de Django ORM). Los casos de uso no saben
    la diferencia: solo conocen la interfaz abstracta.
    """

    def __init__(self, categorias_iniciales=None):
        self._categorias = list(categorias_iniciales or [])
        ids_existentes = [c.id for c in self._categorias if c.id is not None]
        self._siguiente_id = max(ids_existentes, default=0) + 1

    def obtener_por_id(self, categoria_id):
        return next((c for c in self._categorias if c.id == categoria_id), None)

    def listar_para_usuario(self, usuario_id):
        return [
            c for c in self._categorias
            if c.usuario_id is None or c.usuario_id == usuario_id
        ]

    def crear(self, categoria):
        categoria_creada = CategoriaGasto(
            id=self._siguiente_id,
            nombre=categoria.nombre,
            icono=categoria.icono,
            usuario_id=categoria.usuario_id,
        )
        self._categorias.append(categoria_creada)
        self._siguiente_id += 1
        return categoria_creada


class ListarCategoriasUseCaseTests(TestCase):
    def test_devuelve_globales_y_personalizadas_del_usuario(self):
        repo = RepositorioCategoriaGastoFalso([
            CategoriaGasto(id=1, nombre="Vivienda", usuario_id=None),
            CategoriaGasto(id=2, nombre="Mascotas", usuario_id=7),
            CategoriaGasto(id=3, nombre="De otra persona", usuario_id=99),
        ])
        caso_de_uso = ListarCategoriasUseCase(repositorio=repo)

        resultado = caso_de_uso.ejecutar(usuario_id=7)

        nombres = {c.nombre for c in resultado}
        self.assertEqual(nombres, {"Vivienda", "Mascotas"})


class CrearCategoriaPersonalizadaUseCaseTests(TestCase):
    def test_crea_categoria_nueva(self):
        repo = RepositorioCategoriaGastoFalso()
        caso_de_uso = CrearCategoriaPersonalizadaUseCase(repositorio=repo)

        categoria = caso_de_uso.ejecutar(usuario_id=7, nombre="Mascotas")

        self.assertFalse(categoria.es_nueva())
        self.assertEqual(categoria.nombre, "Mascotas")
        self.assertEqual(categoria.usuario_id, 7)

    def test_categoria_duplicada_lanza_excepcion(self):
        repo = RepositorioCategoriaGastoFalso([
            CategoriaGasto(id=1, nombre="Mascotas", usuario_id=7),
        ])
        caso_de_uso = CrearCategoriaPersonalizadaUseCase(repositorio=repo)

        # distinto casing ("mascotas" vs "Mascotas"): igual debe detectarlo
        with self.assertRaises(NombreCategoriaDuplicado):
            caso_de_uso.ejecutar(usuario_id=7, nombre="mascotas")

    def test_mismo_nombre_en_otro_usuario_no_es_duplicado(self):
        repo = RepositorioCategoriaGastoFalso([
            CategoriaGasto(id=1, nombre="Mascotas", usuario_id=7),
        ])
        caso_de_uso = CrearCategoriaPersonalizadaUseCase(repositorio=repo)

        categoria = caso_de_uso.ejecutar(usuario_id=99, nombre="Mascotas")

        self.assertEqual(categoria.usuario_id, 99)
