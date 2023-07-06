from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views
from .views import agregar_compra, cancelar_compra, mostrar_detalle_pedido, validar_cupon
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views

schema_view = get_schema_view(
   openapi.Info(
      title="PachaQtec Hackaton Final Grupo 2",
      default_version='v1',
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

router.register(r'cupones', views.CuponViewSet)
router.register(r'estado_pedidos', views.Estado_PedidoViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'productos', views.ProductoViewSet)
router.register(r'pedidos', views.PedidoViewSet)
router.register(r'detalle_pedidos', views.Detalle_pedidoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api/agregar_compra/<int:producto_id>/<int:user_id>", agregar_compra, name="agregar_compra"),
    path("api/cancelar_compra/<int:producto_id>/<int:user_id>", cancelar_compra, name="cancelar_compra"),
    path("api/mostrar_detalle_pedido/<int:user_id>", mostrar_detalle_pedido, name="mostrar_detalle_pedido"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
