from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PedidoSerializer, CuponSerializer, ValidateCuponSerializer
from rest_framework import permissions
from .models import pedido, cupon

# Create your views here.

class CheckoutViewSet(viewsets.GenericViewSet):
    queryset = pedido.objects.filter(estado=False)
    serializer_class = PedidoSerializer

    @action(detail=False, methods=['post'])
    def validatecupon(self, request):
        serializer = ValidateCuponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cupon = serializer.save()
        data = {
            'codigo': ValidateCuponSerializer(cupon).data
        }
        return Response(data, status=status.HTTP_201_CREATED)
