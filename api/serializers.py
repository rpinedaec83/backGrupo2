from django.contrib.auth.models import User, Group
from django.contrib.auth import password_validation, authenticate
from .models import (
    cupon,
    estado_pedido,
    categoria,
    producto,
    pedido,
    detalle_pedido,
    postular
)
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from users.models import User


class CuponSerializer(serializers.ModelSerializer):
    def retrieve(self, data):
        if not data:
            raise serializers.ValidationError({"data": "No existe Cupon", "error": True})

    class Meta:
        model = cupon
        fields = "__all__"


class Estado_PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = estado_pedido
        fields = "__all__"


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoria
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = producto
        fields = "__all__"

    def create(self, data):
        Producto = producto.objects.create(**data)
        return Producto


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

class PostularSerializer(serializers.ModelSerializer):
    class Meta:
        model = postular
        fields = '__all__'

    def create(self, data):
        Postular = postular.objects.create(**data)
        return Postular