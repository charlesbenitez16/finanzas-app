"""
Modelo Django ORM del modulo planes_financieros. Mapea 1:1 la tabla
`plan_financiero` de 01_schema.sql. managed = False: la tabla ya existe.
FK `usuario` a settings.AUTH_USER_MODEL (mismo gotcha que catalogos).
"""

from django.conf import settings
from django.db import models
from django.db.models import Q


class PlanFinancieroModel(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="planes_financieros",
    )
    nombre = models.CharField(max_length=100, default="Mi plan")
    porcentaje_gasto_fijo = models.DecimalField(max_digits=5, decimal_places=2)
    porcentaje_ahorro = models.DecimalField(max_digits=5, decimal_places=2)
    porcentaje_gasto_libre = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "plan_financiero"
        managed = False
        verbose_name = "Plan financiero"
        verbose_name_plural = "Planes financieros"
        constraints = [
            # uq_plan_activo_usuario: un solo plan activo por usuario.
            models.UniqueConstraint(
                fields=["usuario"],
                condition=Q(activo=True),
                name="uq_plan_activo_usuario",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.nombre} ({'activo' if self.activo else 'inactivo'})"

    # TODO: [el CHECK (suma de porcentajes = 100) vive en 01_schema.sql.
    #        Reflejarlo aca con un CheckConstraint es opcional (managed=False)
    #        y ademas la validacion "de negocio" ya la hace
    #        PlanFinanciero.porcentajes_suman_100() en el dominio.]
