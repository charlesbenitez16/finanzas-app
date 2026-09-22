"""Excepciones de negocio del modulo catalogos."""


class CatalogosError(Exception):
    """Excepcion base para errores de este modulo."""


class CategoriaNoEncontrada(CatalogosError):
    """Se intento operar sobre una categoria que no existe."""


class NombreCategoriaDuplicado(CatalogosError):
    """Ya existe una categoria con ese nombre para el usuario."""


# TODO: agrega aqui las excepciones que necesites a medida que implementes
# los casos de uso (ej. NivelPrioridadNoEncontrado)
