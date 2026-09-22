"""
Modelos Django ORM del modulo catalogos.

Mapean 1:1 las tablas categorias_gasto y niveles_prioridad de
schema_finanzas.sql. Esta es la unica capa que conoce el ORM: el dominio
(domain/entities.py) no importa nada de este archivo.

Nota de diseno: usuario usa settings.AUTH_USER_MODEL (el User de
django.contrib.auth) porque el modulo usuarios todavia no existe. Cuando
lo construyas, vas a tener que decidir si seguis usando el User de Django
o si migras esta FK a tu propio modelo de usuario.

IMPORTANTE: managed = False en ambos modelos. Las tablas categorias_gasto
y niveles_prioridad ya fueron creadas por 01_schema.sql, con sus CHECK
constraints y datos semilla. Con managed=False, Django NUNCA las crea ni
las altera via migrate; simplemente las consulta tal como estan. El
schema SQL sigue siendo la fuente de verdad para la estructura de datos.

GOTCHA PENDIENTE: en 01_schema.sql, categorias_gasto.usuario_id apunta a
tu tabla `usuarios` disenada a mano (con password_hash, etc.), pero aca
abajo el FK usa settings.AUTH_USER_MODEL (el auth_user de Django). Son
DOS TABLAS DISTINTAS. Esto va a funcionar mientras no tengas usuarios
reales, pero es una decision que vas a tener que resolver cuando
construyas el modulo usuarios: o usas el User de Django (y tiras la
tabla usuarios de tu SQL original), o creas tu propio modelo de usuario
en Django (AUTH_USER_MODEL apuntando a tu propia tabla) y migras esta FK.
"""

from django.conf import settings
from django.db import models


class NivelPrioridadModel(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    nivel_orden = models.SmallIntegerField(unique=True)
    descripcion = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "niveles_prioridad"
        managed = False
        verbose_name = "Nivel de prioridad"
        verbose_name_plural = "Niveles de prioridad"

    def __str__(self) -> str:
        return self.nombre


class CategoriaGastoModel(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="categorias_gasto",
        help_text="NULL = categoria global del sistema",
    )
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "categorias_gasto"
        managed = False
        verbose_name = "Categoria de gasto"
        verbose_name_plural = "Categorias de gasto"
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "nombre"], name="uq_categoria_usuario_nombre"
            )
        ]

    def __str__(self) -> str:
        return self.nombre
