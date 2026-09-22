from django.apps import AppConfig


class GastosConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.gastos"
    label = "gastos"
    verbose_name = "Gastos"
