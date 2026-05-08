from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendaViewSet

# Cria o roteador e registra o ViewSet de Vendas
router = DefaultRouter()
router.register(r'vendas', VendaViewSet, basename='venda')

urlpatterns = [
    # Inclui todas as rotas geradas pelo router
    path('', include(router.urls)),
]