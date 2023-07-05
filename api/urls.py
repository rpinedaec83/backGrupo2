from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
# router.register(r'api', views.ApiViewSet, basename='api')

urlpatterns = [path("", include(router.urls))]
