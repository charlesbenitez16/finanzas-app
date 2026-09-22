"""
Corrige un bug heredado de schema_finanzas.sql: ingresos.usuario_id tenia
una FK real de Postgres apuntando a `usuarios` (la tabla de perfil), pero
el codigo Django SIEMPRE usa el id de `auth_user` (request.user.id) como
usuario_id. Quedo enmascarado mientras los ids coincidian por casualidad
entre las dos tablas; al divergir, Postgres empezo a rechazar inserts
validos con ForeignKeyViolation.

Se corre DESPUES de auth.0001_initial (que crea auth_user) para poder
apuntar ahi.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ingresos", "0001_initial"),
        ("auth", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE ingresos DROP CONSTRAINT ingresos_usuario_id_fkey;
                ALTER TABLE ingresos ADD CONSTRAINT ingresos_usuario_id_fkey
                    FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE;
            """,
            reverse_sql="""
                ALTER TABLE ingresos DROP CONSTRAINT ingresos_usuario_id_fkey;
                ALTER TABLE ingresos ADD CONSTRAINT ingresos_usuario_id_fkey
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE;
            """,
        ),
    ]
