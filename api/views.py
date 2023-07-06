from django.contrib.auth.models import User, Group
from api.models import cupon, estado_pedido, categoria, producto, pedido, detalle_pedido
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CuponSerializer, Estado_PedidoSerializer, CategoriaSerializer, ClienteSerializer, ProductoSerializer, PedidoSerializer, detallePedidoSerializer
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from .temp import payment
from django.shortcuts import render

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
    search_fields=['cliente']

class Detalle_pedidoViewSet(viewsets.ModelViewSet):
    
    queryset = detalle_pedido.objects.all()
    serializer_class = detallePedidoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields=['pedido']

def payment(request):
    return render(request, 'payment/index.html')

@csrf_exempt
def charges(request):
    if request.method == 'POST':
        token = request.POST['token']
        installments = request.POST['installments']
        pedido = int(request.POST['idPedido'])
        email = request.POST['email']
        monto = int(request.POST['monto'])
        descrpcion = 'Pago pachaqtec curso online'
        moneda = request.POST['moneda']
        auth_token='sk_test_9dda9590d5943420'
        hed = {'Authorization': 'Bearer ' + auth_token}
        data = {
                    'amount': monto,
                    'currency_code': moneda,
                    'email': email,
                    'source_id':token,
                    'installments':installments,
                    'metadata':{'Descripcion': descrpcion}
                }
        url = 'https://api.culqi.com/v2/charges'
        charge = requests.post(url, json=data, headers=hed)

        print(charge)
        dicRes = {'message':'EXITO'}
        return JsonResponse(charge.json(), safe=False)

    return JsonResponse("only POST method", safe=False)
