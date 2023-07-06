from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="PachaQtec Hackaton Final Grupo 2",
      description="Descripcion de APIS",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
# router.register(r'api', views.ApiViewSet, basename='api')

urlpatterns = [path("", include(router.urls))]
router.register(r'cupones', views.CuponViewSet)
router.register(r'estado_pedidos', views.Estado_pedidoViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'clientes', views.ClienteViewSet)
router.register(r'productos', views.ProductoViewSet)
router.register(r'pedidos', views.PedidoViewSet)
router.register(r'detalle_pedidos', views.Detalle_pedidoViewSet)
