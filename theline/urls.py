from django.urls import path
from theline import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('produtos/', views.produtos_view, name='produtos'),
    path('vendas/', views.vendas_view, name='vendas'),
    path('clientes/', views.clientes_view, name='clientes'),
]