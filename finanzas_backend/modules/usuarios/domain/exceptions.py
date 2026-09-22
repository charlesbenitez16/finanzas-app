"""Excepciones de negocio del modulo usuarios."""


class UsuariosError(Exception):
    """Excepcion base para errores de este modulo."""


class UsuarioNoEncontrado(UsuariosError):
    """Se intento operar sobre un usuario que no existe."""


class EmailYaRegistrado(UsuariosError):
    """Ya existe un usuario con ese email (viola usuarios.email UNIQUE)."""


class CredencialesInvalidas(UsuariosError):
    """El email o la contrasena no coinciden con ningun usuario activo."""


# TODO: [agrega aqui las excepciones que necesites a medida que
#        implementes los casos de uso]
