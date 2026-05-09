from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clientes.views import ClienteViewSet
from produtos.views import ProdutoViewSet 
from vendas.views import VendaViewSet 

router = DefaultRouter()

router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'vendas', VendaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]