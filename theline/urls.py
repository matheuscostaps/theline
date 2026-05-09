from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Certifique-se de que a importação do views aponta para o local correto
# Se este urls.py estiver no mesmo diretório do views.py, use:
from . import views

# Se este arquivo for o core/urls.py e o views estiver no app 'theline', use:
# from theline import views

# ==========================================
# CONFIGURAÇÃO DA API
# ==========================================
router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)
router.register(r'produtos', views.ProdutoViewSet)
router.register(r'vendas', views.VendaViewSet)

# ==========================================
# ROTAS GERAIS
# ==========================================
urlpatterns = [
    # Páginas (Frontend)
    path('', views.dashboard_view, name='dashboard'),
    path('produtos/', views.produtos_view, name='produtos'),
    path('vendas/', views.vendas_view, name='vendas'),

    # Rotas de Ação para Clientes (Sem JS)
    path('clientes/', views.clientes_view, name='clientes'),
    path('clientes/criar/', views.criar_cliente, name='criar_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:pk>/', views.excluir_cliente, name='excluir_cliente'),

    # Rotas HTML do CRUD de Produtos
    path('produtos/', views.produtos_view, name='produtos'),
    path('produtos/criar/', views.criar_produto, name='criar_produto'),
    path('produtos/editar/<int:pk>/', views.editar_produto, name='editar_produto'),
    path('produtos/excluir/<int:pk>/', views.excluir_produto, name='excluir_produto'),

    path('vendas/', views.vendas_view, name='vendas'),
    path('vendas/criar/', views.criar_venda, name='criar_venda'),
    path('vendas/<int:pk>/', views.detalhes_venda, name='detalhes_venda'),
    path('vendas/<int:pk>/adicionar/', views.adicionar_item_venda, name='adicionar_item_venda'),

    path('relatorios/', views.relatorios_view, name='relatorios'),
    # Rotas da API (Retornam JSON)
    path('api/', include(router.urls)),
]