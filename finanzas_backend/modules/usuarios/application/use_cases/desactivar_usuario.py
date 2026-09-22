"""Caso de uso: baja logica de un usuario."""

from dataclasses import dataclass

from modules.usuarios.domain.entities import Usuario
from modules.usuarios.domain.exceptions import UsuarioNoEncontrado
from modules.usuarios.domain.ports.repositories import UsuarioRepository


@dataclass
class DesactivarUsuarioUseCase:
    """
    CONSIGNA
    --------
    Marca un usuario como inactivo (no borra la fila). Si el id no existe,
    lanzar UsuarioNoEncontrado. Usar el metodo de dominio
    Usuario.desactivar() para mutar la entidad y despues persistir con
    repositorio.actualizar().

    Params de ejecutar():
        usuario_id: int
    Retorno: Usuario (ya desactivado)
    """

    repositorio: UsuarioRepository

    def ejecutar(self, usuario_id: int) -> Usuario:
    
        user = self.repositorio.obtener_por_id(usuario_id)
        if user is None:
            raise UsuarioNoEncontrado("No se encontro ningun usuario")

        user.desactivar()

        return self.repositorio.actualizar(user)
