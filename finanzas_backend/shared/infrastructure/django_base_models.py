"""Mixins reutilizables para modelos Django."""

from django.db import models


class TimestampedModel(models.Model):
    """Agrega creado_en / actualizado_en a cualquier modelo que lo herede."""

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
