"""
Migracion inicial del modulo alertas.

STUB a proposito. AlertaPagoModel es managed = False, asi que esta
migracion NO crea ninguna tabla (la tabla `alertas_pago` ya existe por
01_schema.sql). Cuando termines de definir el modelo, regenerala:

    uv run manage.py makemigrations alertas

y revisa que las operaciones queden con "managed": False. Si mantenes las
FK a "servicios_fijos.*" y "gastos.*", makemigrations agregara
dependencias a esas migraciones.
"""

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # TODO: [probablemente ("servicios_fijos", "0001_initial") y
        #        ("gastos", "0001_initial") si mantenes las FK.]
    ]

    operations = [
        # TODO: [regenerar con makemigrations una vez definido AlertaPagoModel.]
    ]
