from users.models import User
from api.models import cupon, estado_pedido, categoria, producto, pedido, detalle_pedido
from rest_framework import viewsets, permissions, status, filters
from .serializers import CuponSerializer, Estado_PedidoSerializer, CategoriaSerializer, ClienteSerializer, ProductoSerializer, PedidoSerializer, detallePedidoSerializer, PostularSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse, Http404
from .templates import payment
from django.shortcuts import render, get_object_or_404
from culqi import __version__
from culqi.client import Culqi
from culqi.resources import Card, Customer, Charge
import json
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes

from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes


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

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

    def create(self, request, *args, **kwargs):
        serializer = ProductoSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        exp = serializer.save()
        data = ProductoSerializer(exp).data
        return Response(data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

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

public_key = "pk_test_89a1417406ce7fa2"
private_key = "sk_test_SWyklAB8rIyjXmje"

def payment(request):
     return render(request, 'payment/index.html')


@csrf_exempt
@permission_classes(["AllowAny"])
def generateCharge(request):
    if request.method == 'POST':
        body = request.json
        version = __version__

        culqi = Culqi(public_key, private_key)
        charge = Charge(client=culqi)
        card = charge.create(body)
        print(card["data"])
        return HttpResponse(json.dumps(card["data"]), content_type="application/json")
    return JsonResponse("only POST method", safe=False)

# @csrf_exempt
# def generateCharge(request):
#     if request.method == 'POST':
#         token = request.POST['token']
#         installments = request.POST['installments']
#         pedido = int(request.POST['idPedido'])
#         email = request.POST['email']
#         monto = int(request.POST['monto'])
#         descripcion = 'Pago pachaqtec curso online'
#         moneda = request.POST['moneda']
#         auth_token='sk_test_SWyklAB8rIyjXmje'
#         hed = {'Authorization': 'Bearer ' + auth_token}
#         data = {
#                     'amount': monto,
#                     'currency_code': moneda,
#                     'email': email,
#                     'source_id':token,
#                     'installments':installments,
#                     'metadata':{'Descripcion': descripcion}
#                 }
#         url = 'https://api.culqi.com/v2/charges'
#         charge = requests.post(url, json=data, headers=hed)
#         # print(charge)
#         dicRes = {'message':'EXITO'}
#         return JsonResponse(charge.json(), safe=False)
#     return JsonResponse("only POST method", safe=False)

@api_view(["GET"])
def agregar_compra(request, producto_id, user_id):
    try:
        cliente_ = get_object_or_404(User, id=user_id)
        estado_ = estado_pedido.objects.get(descripcion="pendiente")
        pedido_ = pedido.objects.get_or_create(
            cliente=cliente_,
            estado = estado_,
            defaults={'subtotal':0,'igv':0,'total':0,'cupon':None}
        )
        producto_ = get_object_or_404(producto, id = producto_id)
        pedido_.estado = "completado"
        pedido_[0].save()
        detalle_nuevo = detalle_pedido(pedido=pedido_[0], producto = producto_, cantidad=1, subtotal=producto_.precio)
        detalle_nuevo.save()
        serializer = detallePedidoSerializer(detalle_nuevo)
    except Http404 as error:
        print(str(error))
    return Response(serializer.data)

def cancelar_compra(request, producto_id, user_id):
    cliente_ = get_object_or_404(User, id=user_id)
    pedido_ = get_object_or_404(pedido, cliente = cliente_)
    producto_ = get_object_or_404(producto, id = producto_id)
    detalle_pedido_ = detalle_pedido.objects.filter(pedido=pedido_, producto=producto_)
    pedido_.estado = "anulado"
    pedido_.save()
    detalle_pedido_.delete()
    serializer = detallePedidoSerializer(detalle_pedido_)
    return Response(serializer.data)

@api_view(["GET"])
def mostrar_detalle_pedido(request, user_id):
    cliente_ = get_object_or_404(User, id=user_id)
    pedido_ = get_object_or_404(pedido, cliente = cliente_)
    detalle_pedido_ = detalle_pedido.objects.filter(pedido=pedido_)
    serializer = detallePedidoSerializer(detalle_pedido_)
    return Response(serializer.data)

def validar_cupon(request, cupon_id):
    cupon_ = get_object_or_404(cupon, codigo = cupon_id)
    serializer = CuponSerializer(cupon_)
    return Response(serializer.data)

@api_view(["GET"])
def PorductoView(req):
    productos = producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def CategoriaView(req):
    categorias = categoria.objects.filter()
    serializer = CategoriaSerializer(categorias, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def ProductoView(req):
    productos = producto.objects.filter(categoria_id=1)
    serializer = CategoriaSerializer(productos, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def PriceView(req):
    productos = producto.objects.filter(precio=600)
    serializer = ProductoSerializer(productos, many = True)
    return Response(serializer.data)

def ProductoByCategoriaView(req, categoria):
    productos = producto.objects.filter(categoria = categoria)
    serializer = ProductoSerializer(productos, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def BuscarProductoView(req, nombre):
    productos = producto.objects.filter(nombre = nombre)
    serializer = ProductoSerializer(productos, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def ProductoByIdView(req, id):
    productos = producto.objects.filter(id = id)
    serializer = ProductoSerializer(productos, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def PostularView(request):
    serializer = PostularSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Datos enviados correctamente.'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
def compras_realizadas(request):
    pedido_ = pedido.objects.filter(estado_pedido = "completado")
    serializer = PedidoSerializer(pedido_)
    return Response(serializer.data)
