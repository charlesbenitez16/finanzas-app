"""
Modelo Django ORM del modulo alertas. Mapea 1:1 la tabla `alertas_pago`
de 01_schema.sql. managed = False: la tabla ya existe.

FK a otros bounded contexts (servicio_fijo -> servicios_fijos, gasto ->
gastos): mismo criterio que en los demas modulos. Si preferis desacoplar,
cambia por IntegerField y valida en el caso de uso.
"""

from django.conf import settings
from django.db import models


class AlertaPagoModel(models.Model):
    ESTADOS = (
        ("Pendiente", "Pendiente"),
        ("Enviada", "Enviada"),
        ("Leida", "Leida"),
        ("Resuelta", "Resuelta"),
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="alertas_pago",
    )
    servicio_fijo = models.ForeignKey(
        "servicios_fijos.ServicioFijoModel",
        on_delete=models.CASCADE,
        related_name="alertas",
        db_column="servicio_fijo_id",
    )
    gasto = models.ForeignKey(
        "gastos.GastoModel",
        on_delete=models.SET_NULL,
        related_name="alertas_resueltas",
        db_column="gasto_id",
        blank=True,
        null=True,
    )
    periodo_mes = models.SmallIntegerField()
    periodo_anio = models.SmallIntegerField()
    fecha_alerta = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Pendiente")
    mensaje = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "alertas_pago"
        managed = False
        verbose_name = "Alerta de pago"
        verbose_name_plural = "Alertas de pago"
        indexes = [
            models.Index(
                fields=["usuario", "estado"], name="idx_alertas_usuario_estado"
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["servicio_fijo", "periodo_anio", "periodo_mes"],
                name="uq_alerta_servicio_periodo",
            ),
        ]

    def __str__(self) -> str:
        return f"Alerta {self.servicio_fijo_id} {self.periodo_mes}/{self.periodo_anio} ({self.estado})"

    # TODO: [CHECK (estado IN (...)) vive en 01_schema.sql; reflejarlo aca
    #        es opcional (managed=False).]
