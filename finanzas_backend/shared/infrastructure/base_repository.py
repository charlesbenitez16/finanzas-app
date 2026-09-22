"""
Utilidades reutilizables para implementar repositorios sobre Django ORM.

Vive en infrastructure/ (no en domain/) porque conoce Django. Las
interfaces de los repositorios (los "puertos") se definen en el
domain/ports/repositories.py de cada modulo; esta clase es una base
opcional para reducir codigo repetido al implementarlas.
"""

from typing import Generic, TypeVar

from django.db.models import Model

ModeloDjango = TypeVar("ModeloDjango", bound=Model)


class DjangoRepositoryBase(Generic[ModeloDjango]):
    model: type[ModeloDjango]

    def _obtener_queryset(self):
        # TODO: devolver self.model.objects.all() (o un queryset mas
        # especifico si el repositorio concreto lo necesita)
        raise NotImplementedError
