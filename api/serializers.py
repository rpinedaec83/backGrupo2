from django.contrib.auth.models import User, Grou
from django.contrib.auth import password_validation, authenticate
from .models import (
    cupon,
    estado_pedido,
    categoria,
    producto,
    pedido,
    detalle_pedido,
)
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users.models import User


class CuponSerializer(serializers.HyperlinkedModelSerializer):
    def retrieve(self, data):
        if not data:
            raise serializers.ValidationError({"data": "No existe Cupon", "error": True})

    class Meta:
        model = cupon
        fields = "__all__"


class Estado_PedidoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = estado_pedido
        fields = "__all__"


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = categoria
        fields = "__all__"


class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = producto
        fields = "__all__"

class PedidoSerializer(serializers.ModelSerializer):
    def retrieve(self, data):
        if not data:
            raise serializers.ValidationError({"data": "No existen Pedidos", "error": True})
    class Meta:
        model = pedido
        fields = '__all__'

class detallePedidoSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if not data["pedido"]:
            raise serializers.ValidationError({"data": "Se requiere # de Pedido para detalle", "error": True})
        return data
    class Meta:
        model = detalle_pedido
        fields = '__all__'