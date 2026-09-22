"""
Migracion inicial del modulo gastos.

STUB a proposito. GastoModel es managed = False, asi que esta migracion
NO crea ninguna tabla (la tabla `gastos` ya existe por 01_schema.sql).
Cuando termines de definir el modelo, regenerala:

    uv run manage.py makemigrations gastos

y revisa que las operaciones queden con "managed": False. Si mantenes las
FK a "catalogos.*" y "servicios_fijos.*", makemigrations agregara
dependencias a esas migraciones.
"""

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # TODO: [probablemente ("catalogos", "0001_initial") y
        #        ("servicios_fijos", "0001_initial") si mantenes las FK.]
    ]

    operations = [
        # TODO: [regenerar con makemigrations una vez definido GastoModel.]
    ]
