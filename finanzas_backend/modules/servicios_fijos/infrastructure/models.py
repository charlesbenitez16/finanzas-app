"""
Modelo Django ORM del modulo servicios_fijos. Mapea 1:1 la tabla
`servicios_fijos` de 01_schema.sql. managed = False: la tabla ya existe.

Sobre las FK a otro bounded context (categoria, prioridad -> modulo
catalogos): aca se usan ForeignKey con referencia por string
("catalogos.CategoriaGastoModel"). Es lo mas parecido al schema real.
Si preferis DESACOPLAR los modulos, cambia esas dos por
models.IntegerField(db_column="categoria_id") / ("prioridad_id") y valida
la existencia en el caso de uso contra los repos de catalogos. Deja
constancia de tu decision.
"""

from django.conf import settings
from django.db import models


class ServicioFijoModel(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="servicios_fijos",
    )
    categoria = models.ForeignKey(
        "catalogos.CategoriaGastoModel",
        on_delete=models.PROTECT,
        related_name="servicios_fijos",
        db_column="categoria_id",
    )
    prioridad = models.ForeignKey(
        "catalogos.NivelPrioridadModel",
        on_delete=models.PROTECT,
        related_name="servicios_fijos",
        db_column="prioridad_id",
    )
    nombre = models.CharField(max_length=150)
    dia_vencimiento = models.SmallIntegerField()
    monto_estimado = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    es_monto_variable = models.BooleanField(default=False)
    dias_anticipacion_alerta = models.SmallIntegerField(default=3)
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "servicios_fijos"
        managed = False
        verbose_name = "Servicio fijo"
        verbose_name_plural = "Servicios fijos"
        indexes = [
            models.Index(fields=["usuario"], name="idx_servicios_usuario"),
        ]

    def __str__(self) -> str:
        return self.nombre

    # TODO: [CHECK (dia_vencimiento BETWEEN 1 AND 31) y
    #        (monto_estimado >= 0) viven en 01_schema.sql. Reflejarlos en
    #        Meta.constraints es opcional (managed=False).]
