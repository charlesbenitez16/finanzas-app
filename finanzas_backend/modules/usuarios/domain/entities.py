"""
Entidad de dominio del modulo usuarios: Usuario.

Python puro (dataclass), sin ningun import de Django. Mapea la tabla
`usuarios` de schema_finanzas.sql (id, nombre, email, password_hash,
fecha_registro, activo). Es el "dueno" del resto de los modulos:
ingresos, gastos, servicios_fijos, planes_financieros y alertas cuelgan
de un usuario_id.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from shared.domain.base_entity import Entity


@dataclass
class Usuario(Entity):
    """
    Usuario del sistema de finanzas personales.

    CONSIGNA
    --------
    Aca solo vive comportamiento que el Usuario puede resolver MIRANDO
    SUS PROPIOS ATRIBUTOS (mismo criterio que CategoriaGasto.es_global()
    en catalogos): nada que necesite consultar la base de datos ni ver a
    otros usuarios.

    Campos (ver 01_schema.sql tabla `usuarios`):
        nombre         -- nombre visible (VARCHAR 150, NOT NULL)
        email          -- unico en la tabla (VARCHAR 150, UNIQUE)
        password_hash  -- hash ya calculado; el dominio NUNCA ve la
                          contrasena en claro
        fecha_registro -- timestamp de alta (la base lo pone con DEFAULT NOW())
        activo         -- baja logica (BOOLEAN, DEFAULT TRUE)
        auth_user_id   -- id del django.contrib.auth.User vinculado (el
                          que realmente autentica: sesion/Basic/JWT).
                          Lo crea y lo une infrastructure/repositories.py.
    """

    nombre: str = ""
    email: str = ""
    password_hash: str = ""
    fecha_registro: Optional[datetime] = None
    activo: bool = True
    auth_user_id: Optional[int] = None

    def esta_activo(self) -> bool:
        """
        CONSIGNA: devolver True si este usuario puede operar en el sistema.

        Retorno: bool
        """
        if self.activo:
            return self.activo
        return False
    def desactivar(self) -> None:
        """
        CONSIGNA: dar de baja logica al usuario (la fila NO se borra).
        Muta el estado de la entidad en memoria; persistir es
        responsabilidad del repositorio / caso de uso.

        Retorno: None
        """
        
        self.activo = False
