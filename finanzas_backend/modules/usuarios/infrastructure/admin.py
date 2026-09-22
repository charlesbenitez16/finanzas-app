from django.contrib import admin

from modules.usuarios.infrastructure.models import UsuarioModel


@admin.register(UsuarioModel)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "email", "activo", "fecha_registro")
    list_filter = ("activo",)
    search_fields = ("nombre", "email")
    # TODO: [password_hash no deberia editarse a mano desde el admin;
    #        considera readonly_fields o excluirlo.]
