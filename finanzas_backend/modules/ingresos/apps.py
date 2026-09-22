from django.apps import AppConfig


class IngresosConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.ingresos"
    label = "ingresos"
    verbose_name = "Ingresos"
