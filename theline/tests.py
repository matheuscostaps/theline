from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Cliente, ItemVenda, Venda, Produto
from django.core.exceptions import ValidationError

class ClienteAPITest(APITestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Ana Silva", 
            cpf="98765432100", 
            email="ana@teste.com"
        )

        self.url = reverse('cliente-list') 

    def test_get_lista_clientes(self):
        """Garante que a API retorna status 200 ao listar clientes"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProdutoTests(APITestCase):

    def setUp(self):
        self.produto = Produto.objects.create(
            nome="Pijama de Poney",
            preco=250.00,
            quantidade_estoque=10
        )
        self.url_list = reverse('produto-list') 
        self.url_detail = reverse('produto-detail', kwargs={'pk': self.produto.pk})
        self.url_baixar_estoque = reverse('produto-baixar-estoque', kwargs={'pk': self.produto.pk})

    ## --- Testes de Lógica de Modelo --- ##

    def test_baixar_estoque_sucesso_model(self):
        """Testa o método baixar_estoque diretamente no modelo."""
        self.produto.baixar_estoque(5)
        self.assertEqual(self.produto.quantidade_estoque, 5)

    def test_baixar_estoque_insuficiente_model(self):
        """Testa se o erro de validação é lançado quando o estoque é insuficiente."""
        with self.assertRaises(ValidationError):
            self.produto.baixar_estoque(11)

    ## --- Testes de API (ViewSet) --- ##

    def test_listar_produtos(self):
        """Testa o endpoint GET /produtos/"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_criar_produto(self):
        """Testa o endpoint POST /produtos/"""
        data = {'nome': 'Mouse Pad', 'preco': 50.00, 'quantidade_estoque': 100}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_action_baixar_estoque_sucesso(self):
        """Testa o endpoint POST /produtos/{id}/baixar_estoque/"""
        data = {'quantidade': 3}
        response = self.client.post(self.url_baixar_estoque, data)
        
        self.produto.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.produto.quantidade_estoque, 7)
        self.assertEqual(response.data['status'], 'estoque atualizado')

    def test_action_baixar_estoque_erro(self):
        """Testa a falha na API ao tentar baixar mais do que o disponível."""
        data = {'quantidade': 20}
        response = self.client.post(self.url_baixar_estoque, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class VendaViewSetTests(APITestCase):

    def setUp(self):
        # Criando dados básicos para os testes
        self.cliente = Cliente.objects.create(nome="João Silva")
        self.produto = Produto.objects.create(
            nome="Pijama de Poney",
            preco=100.00,
            quantidade_estoque=50
        )

        self.produto = Produto.objects.create(
            nome="Pijama de Poney", 
            preco=100.00,
            quantidade_estoque=50 
        )

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
