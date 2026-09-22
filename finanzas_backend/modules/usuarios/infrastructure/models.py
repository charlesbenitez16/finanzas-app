"""
Modelo Django ORM del modulo usuarios.

Mapea 1:1 la tabla `usuarios` de schema_finanzas.sql. Unica capa que
conoce el ORM: el dominio (domain/entities.py) no importa nada de aca.

managed = False: la tabla `usuarios` ya fue creada por 01_schema.sql.
Django solo la consulta, nunca la crea ni la altera con migrate.

RESUELTO: el resto de los modulos usa settings.AUTH_USER_MODEL
(auth_user de Django) para sus FK `usuario`, que es una tabla distinta de
esta `usuarios` hecha a mano (con password_hash, etc.). En vez de migrar
todas esas FK, `usuarios` pasa a ser el "perfil" de un auth.User: cada
fila de `usuarios` apunta a su auth.User via `auth_user_id`.
DjangoUsuarioRepository.crear() crea las dos filas juntas (ver ese
archivo). `auth_user_id` NO tiene FK real a nivel de base (ver el
comentario en schema_finanzas.sql): la referencia la garantiza la app.
"""

from django.conf import settings
from django.db import models


class UsuarioModel(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    auth_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="auth_user_id",
        null=True,
        blank=True,
        # Sin constraint real en la base: la tabla `usuarios` la carga
        # schema_finanzas.sql ANTES de que exista auth_user (esa la crea
        # migrate, despues). db_constraint=False le dice a Django que no
        # intente crear/asumir un FK de verdad en el esquema.
        db_constraint=False,
        related_name="perfil_finanzas",
    )

    class Meta:
        db_table = "usuarios"
        managed = False
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self) -> str:
        return self.email
