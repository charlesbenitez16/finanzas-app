from django.apps import AppConfig


class ServiciosFijosConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.servicios_fijos"
    label = "servicios_fijos"
    verbose_name = "Servicios fijos"
