from django.contrib.auth.models import User, Group
from api.models import cupon, estado_pedido, categoria, producto, pedido, detalle_pedido
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import CuponSerializer, Estado_PedidoSerializer, CategoriaSerializer, ClienteSerializer, ProductoSerializer, PedidoSerializer, Detalle_PedidoSerializer
from rest_framework import filters

class CuponViewSet(viewsets.ModelViewSet):
    
    queryset = cupon.objects.all()
    serializer_class = CuponSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['codigo']

class Estado_PedidoViewSet(viewsets.ModelViewSet):
    
    queryset = estado_pedido.objects.all()
    serializer_class = Estado_PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['descripcion']

class CategoriaViewSet(viewsets.ModelViewSet):
    
    queryset = categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

# class ClienteViewSet(viewsets.ModelViewSet):
   
#     queryset = cliente.objects.all()
#     serializer_class = ClienteSerializer
#     permission_classes = [permissions.IsAuthenticated]    
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['nombre']

class ProductoViewSet(viewsets.ModelViewSet):
  
    queryset = producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class PedidoViewSet(viewsets.ModelViewSet):
    
    queryset = pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]

class Detalle_pedidoViewSet(viewsets.ModelViewSet):
    
    queryset = detalle_pedido.objects.all()
    serializer_class = Detalle_PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
