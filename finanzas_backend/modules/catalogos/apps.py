from django.apps import AppConfig


class CatalogosConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.catalogos"
    label = "catalogos"
    verbose_name = "Catalogos"
