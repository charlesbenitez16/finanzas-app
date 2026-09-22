"""
Modelo Django ORM del modulo gastos. Mapea 1:1 la tabla `gastos` de
01_schema.sql. managed = False: la tabla ya existe.

FK a otros bounded contexts (categoria, prioridad -> catalogos;
servicio_fijo -> servicios_fijos): igual criterio que en
modules/servicios_fijos/infrastructure/models.py. Si preferis desacoplar,
cambia por IntegerField y valida en el caso de uso.
"""

from django.conf import settings
from django.db import models
from django.db.models import Q


class GastoModel(models.Model):
    ESTADOS = (
        ("Pagado", "Pagado"),
        ("Pendiente", "Pendiente"),
        ("Vencido", "Vencido"),
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gastos",
    )
    categoria = models.ForeignKey(
        "catalogos.CategoriaGastoModel",
        on_delete=models.PROTECT,
        related_name="gastos",
        db_column="categoria_id",
    )
    servicio_fijo = models.ForeignKey(
        "servicios_fijos.ServicioFijoModel",
        on_delete=models.SET_NULL,
        related_name="pagos",
        db_column="servicio_fijo_id",
        blank=True,
        null=True,
    )
    prioridad = models.ForeignKey(
        "catalogos.NivelPrioridadModel",
        on_delete=models.PROTECT,
        related_name="gastos",
        db_column="prioridad_id",
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_gasto = models.DateField()
    periodo_mes = models.SmallIntegerField()
    periodo_anio = models.SmallIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Pagado")
    descripcion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "gastos"
        managed = False
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        indexes = [
            models.Index(
                fields=["usuario", "periodo_anio", "periodo_mes"],
                name="idx_gastos_usuario_periodo",
            ),
            models.Index(fields=["servicio_fijo"], name="idx_gastos_servicio"),
        ]
        constraints = [
            # uq_gasto_servicio_periodo: unico por (servicio_fijo, periodo)
            # solo cuando servicio_fijo_id IS NOT NULL (indice parcial en SQL).
            models.UniqueConstraint(
                fields=["servicio_fijo", "periodo_anio", "periodo_mes"],
                condition=Q(servicio_fijo__isnull=False),
                name="uq_gasto_servicio_periodo",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.descripcion or 'Gasto'} {self.monto} ({self.periodo_mes}/{self.periodo_anio})"

    # TODO: [CHECK (monto > 0) y CHECK (estado IN (...)) viven en
    #        01_schema.sql. Reflejarlos aca es opcional (managed=False).]
