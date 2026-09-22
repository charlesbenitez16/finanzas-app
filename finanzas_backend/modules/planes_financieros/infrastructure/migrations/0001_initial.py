"""
Migracion inicial del modulo planes_financieros.

STUB a proposito. PlanFinancieroModel es managed = False, asi que esta
migracion NO crea ninguna tabla (la tabla `plan_financiero` ya existe
por 01_schema.sql). Cuando termines de definir el modelo, regenerala:

    uv run manage.py makemigrations planes_financieros

y revisa que las operaciones queden con "managed": False.
"""

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        # TODO: [regenerar con makemigrations una vez definido PlanFinancieroModel.]
    ]
