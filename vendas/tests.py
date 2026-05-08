from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Venda, ItemVenda
from clientes.models import Cliente
from produtos.models import Produto
from decimal import Decimal

class VendaViewSetTests(APITestCase):

    def setUp(self):
        # Criando dados básicos para os testes
        self.cliente = Cliente.objects.create(nome="João Silva")
        self.produto = Produto.objects.create(nome="Pijama de Poney", preco=100.00)
        
        # Criando uma venda inicial
        self.venda = Venda.objects.create(
            cliente=self.cliente,
            valor_total=Decimal('150.00')
        )
        self.item = ItemVenda.objects.create(
            venda=self.venda,
            produto=self.produto,
            quantidade=1,
            preco_unitario=Decimal('150.00')
        )
        
        self.url_list = reverse('venda-list')  
        self.url_relatorio = reverse('venda-relatorio')

    def test_list_vendas(self):
        """Testa se a listagem de vendas está funcionando"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_relatorio_calculos_corretos(self):
        """Testa se a agregação do relatório (Soma, Média, Contagem) está correta"""
        # Criando uma segunda venda para validar a média e faturamento
        venda2 = Venda.objects.create(cliente=self.cliente, valor_total=Decimal('50.00'))
        
        response = self.client.get(self.url_relatorio)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
       # Faturamento esperado: 150 + 50 = 200
        self.assertEqual(response.data['indicadores']['faturamento_total'], Decimal('200.00'))   
        self.assertEqual(response.data['indicadores']['ticket_medio'], Decimal('100.00')) 
        # Quantidade esperada: 2
        self.assertEqual(response.data['indicadores']['quantidade_vendas'], 2) 

    def test_relatorio_vazio(self):
        """Testa o comportamento do relatório quando não existem vendas"""
        Venda.objects.all().delete()
        
        response = self.client.get(self.url_relatorio)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['indicadores']['faturamento_total'], 0)
        self.assertEqual(response.data['indicadores']['ticket_medio'], 0) 
        self.assertEqual(response.data['indicadores']['quantidade_vendas'], 0) 

    def test_create_venda_invalid_data(self):
        """Testa tentativa de criar venda sem cliente"""
        data = {"valor_total": "10.00"}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)