from django.apps import AppConfig


class PlanesFinancierosConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.planes_financieros"
    label = "planes_financieros"
    verbose_name = "Planes financieros"
