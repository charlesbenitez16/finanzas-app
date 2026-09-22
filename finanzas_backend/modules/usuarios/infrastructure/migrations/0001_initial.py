"""
Migracion inicial del modulo usuarios.

STUB a proposito. UsuarioModel es managed = False, asi que esta
migracion NO crea ninguna tabla (la tabla `usuarios` ya existe por
01_schema.sql). Cuando termines de definir los campos del modelo,
regenerala para que el estado de migraciones de Django quede consistente:

    uv run manage.py makemigrations usuarios

y revisa que las operaciones queden con "managed": False, igual que en
modules/catalogos/infrastructure/migrations/0001_initial.py.
"""

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        # TODO: [regenerar con makemigrations una vez definido UsuarioModel.]
    ]
