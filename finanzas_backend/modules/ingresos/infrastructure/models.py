"""
Modelo Django ORM del modulo ingresos. Mapea 1:1 la tabla `ingresos` de
01_schema.sql. managed = False: la tabla ya existe, Django solo la
consulta. La FK `usuario` apunta a settings.AUTH_USER_MODEL por el mismo
motivo (y con el mismo gotcha pendiente) que en catalogos: ver
modules/catalogos/infrastructure/models.py y modules/usuarios/.
"""

from django.conf import settings
from django.db import models


class IngresoModel(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ingresos",
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    periodo_mes = models.SmallIntegerField()
    periodo_anio = models.SmallIntegerField()
    fuente = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ingresos"
        managed = False
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"
        indexes = [
            models.Index(
                fields=["usuario", "periodo_anio", "periodo_mes"],
                name="idx_ingresos_usuario_periodo",
            )
        ]

    def __str__(self) -> str:
        return f"{self.fuente or 'Ingreso'} {self.periodo_mes}/{self.periodo_anio}"

    # TODO: [el CHECK (monto > 0) y (periodo_mes BETWEEN 1 AND 12) viven en
    #        01_schema.sql (fuente de verdad). Si queres reflejarlos aca
    #        como constraints, agregalos en Meta.constraints; con
    #        managed=False son solo documentacion para Django.]
