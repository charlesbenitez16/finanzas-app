"""
Serializers DRF del modulo catalogos.

CORRECCION IMPORTANTE respecto a la version anterior: estos son
serializers.Serializer simples, NO ModelSerializer.

Por que: un ModelSerializer(model=CategoriaGastoModel) genera sus campos
mirando el modelo Django -- para una ForeignKey como "usuario", genera un
campo que espera un atributo `usuario` (la relacion completa) en la
instancia que le pases. Pero nosotros le pasamos una entidad de dominio
CategoriaGasto, que solo tiene `usuario_id` (un int plano), no `usuario`.
Eso rompe en tiempo de ejecucion con un AttributeError.

Mas alla de arreglar el error puntual, esto es coherente con la
arquitectura: el serializer es parte de interfaces/ (adaptador primario)
y no deberia conocer el modelo ORM de infrastructure/ en absoluto. Define
la forma de los datos que entran y salen por HTTP, que es la forma de la
entidad de dominio -- no la forma de la tabla.
"""

from rest_framework import serializers


class NivelPrioridadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=50)
    nivel_orden = serializers.IntegerField()
    descripcion = serializers.CharField(
        max_length=None, required=False, allow_null=True, allow_blank=True
    )
    color = serializers.CharField(
        max_length=20, required=False, allow_null=True, allow_blank=True
    )


class CategoriaGastoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    usuario_id = serializers.IntegerField(read_only=True, allow_null=True)
    nombre = serializers.CharField(max_length=100)
    icono = serializers.CharField(
        max_length=50, required=False, allow_null=True, allow_blank=True
    )
