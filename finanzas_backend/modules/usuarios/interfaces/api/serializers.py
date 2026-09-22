"""
Serializers DRF del modulo usuarios.

Son serializers.Serializer SIMPLES, no ModelSerializer: describen la
forma de la ENTIDAD DE DOMINIO (Usuario) que entra/sale por HTTP, no la
forma de la tabla. Ver la explicacion completa en
modules/catalogos/interfaces/api/serializers.py.

REGLA DE ORO: password_hash NUNCA sale en una respuesta. La contrasena
en claro solo entra (write_only).
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class UsuarioSerializer(serializers.Serializer):
    """Salida: lo que la API devuelve de un Usuario."""

    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=150)
    fecha_registro = serializers.DateTimeField(read_only=True)
    activo = serializers.BooleanField(read_only=True)




class RegistroUsuarioSerializer(serializers.Serializer):
    """Entrada de POST /api/usuarios/registro/."""

    nombre = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    def validate_password(self, value):
        validate_password(value)
        return value

class LoginSerializer(serializers.Serializer):
    """Entrada de POST /api/usuarios/login/."""

    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(write_only=True)


class TokenAuthSerializer(serializers.Serializer):
    """
    Salida de registro/login: el usuario + el par de tokens JWT.
    El front guarda `access` y lo manda como
    'Authorization: Bearer <access>' en cada request. Cuando expira
    (ACCESS_TOKEN_LIFETIME, ver settings), usa `refresh` contra
    POST /api/usuarios/token/refresh/ para obtener un access nuevo sin
    volver a pedir la contrasena.
    """

    usuario = UsuarioSerializer()
    access = serializers.CharField()
    refresh = serializers.CharField()
