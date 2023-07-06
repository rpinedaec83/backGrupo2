from users.models import User
from api.models import cupon, estado_pedido, categoria, producto, pedido, detalle_pedido
from rest_framework import viewsets, permissions
from .serializers import CuponSerializer, Estado_PedidoSerializer, CategoriaSerializer, ClienteSerializer, ProductoSerializer, PedidoSerializer, detallePedidoSerializer
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse, Http404
from .temp import payment
from django.shortcuts import render, get_object_or_404

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
        descripcion = 'Pago pachaqtec curso online'
        moneda = request.POST['moneda']
        auth_token='sk_test_9dda9590d5943420'
        hed = {'Authorization': 'Bearer ' + auth_token}
        data = {
                    'amount': monto,
                    'currency_code': moneda,
                    'email': email,
                    'source_id':token,
                    'installments':installments,
                    'metadata':{'Descripcion': descripcion}
                }
        url = 'https://api.culqi.com/v2/charges'
        charge = requests.post(url, json=data, headers=hed)

        print(charge)
        dicRes = {'message':'EXITO'}
        return JsonResponse(charge.json(), safe=False)

    return JsonResponse("only POST method", safe=False)

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

        pedido_[0].save()

        detalle_nuevo = detalle_pedido(pedido=pedido_[0], producto = producto_, cantidad=1, subtotal=producto_.precio)
        detalle_nuevo.save()
    except Http404 as error:
        print(str(error))
    return render(request, "agregar_producto.html")

def cancelar_compra(request, producto_id, user_id):
    cliente_ = get_object_or_404(User, id=user_id)
    pedido_ = get_object_or_404(pedido, cliente = cliente_)
    producto_ = get_object_or_404(producto, id = producto_id)
    detalle_pedido_ = detalle_pedido.objects.filter(pedido=pedido_, producto=producto_)
    pedido_.estado = "anulado"
    pedido_.save()
    detalle_pedido_.delete()
    return render(request, "agregar_producto.html")

def mostrar_detalle_pedido(request, user_id):
    cliente_ = get_object_or_404(User, id=user_id)
    pedido_ = get_object_or_404(pedido, cliente = cliente_)
    detalle_pedido_ = detalle_pedido.objects.filter(pedido=pedido_)
    return render(request, "detalle_producto.html", {'detalle_pedido_':detalle_pedido_})

def validar_cupon(request, cupon_id):
    cupon_ = get_object_or_404(cupon, codigo = cupon_id)
    return render(request)
