"""
Migracion inicial del modulo servicios_fijos.

STUB a proposito. ServicioFijoModel es managed = False, asi que esta
migracion NO crea ninguna tabla (la tabla `servicios_fijos` ya existe
por 01_schema.sql). Cuando termines de definir el modelo, regenerala:

    uv run manage.py makemigrations servicios_fijos

y revisa que las operaciones queden con "managed": False. Ojo: si dejas
las ForeignKey a "catalogos.*", makemigrations agregara una dependencia
a la migracion de catalogos.
"""

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # TODO: [si mantenes las FK a catalogos, quedara algo como
        #        ("catalogos", "0001_initial") aca.]
    ]

    operations = [
        # TODO: [regenerar con makemigrations una vez definido ServicioFijoModel.]
    ]
