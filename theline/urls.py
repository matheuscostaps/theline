from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD

# Certifique-se de que a importação do views aponta para o local correto
# Se este urls.py estiver no mesmo diretório do views.py, use:
from . import views

# Se este arquivo for o core/urls.py e o views estiver no app 'theline', use:
# from theline import views

=======
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

>>>>>>> estilizacao
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
<<<<<<< HEAD
    # Páginas (Frontend)
    path('', views.dashboard_view, name='dashboard'),
=======
    path('', views.dashboard, name='dashboard'),

    # Páginas (Frontend)
>>>>>>> estilizacao
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
<<<<<<< HEAD
=======

    # permitir o fluxo de login
    path('login/', views.login_view, name='login'),
    # permitir o fluxo de login
    path('logout/', views.logout_view, name='logout'), 
    # permitir o cadastro de um novo usuário
    path('register/', views.register_view, name='register'),

    path('api/busca-global/', views.busca_global, name='busca_global'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
>>>>>>> estilizacao
]