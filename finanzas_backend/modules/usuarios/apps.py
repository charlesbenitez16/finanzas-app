from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.usuarios"
    label = "usuarios"
    verbose_name = "Usuarios"
