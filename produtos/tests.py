from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError
from .models import Produto

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
