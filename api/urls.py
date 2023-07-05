"""api URLs"""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from api import views

router = DefaultRouter()
# router.register(r'api', views.ApiViewSet, basename='api')

urlpatterns = [path("", include(router.urls))]
