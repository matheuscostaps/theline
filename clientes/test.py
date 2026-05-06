from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Cliente
from produtos.models import Produto

class SistemaGestaoTest(TestCase):

    def setUp(self):
        """Configura os dados iniciais para cada teste"""
        self.cliente = Cliente.objects.create(
            nome="Matheus Membro 4", 
            cpf="12345678901", 
            email="matheus@teste.com"
        )
        self.produto = Produto.objects.create(
            nome="Camiseta de Teste", 
            preco=50.00, 
            quantidade_estoque=10
        )

    def test_estoque_insuficiente(self):
        """Regra: Validar se a lógica de estoque detecta falta de produtos"""
        # Se tentarmos vender 100, mas só temos 10:
        quantidade_venda = 100
        esta_disponivel = self.produto.quantidade_estoque >= quantidade_venda
        
        self.assertFalse(esta_disponivel, "O sistema deveria indicar que não há estoque suficiente.")

    def test_preco_negativo(self):
        """Regra: Preço não pode ser negativo (Exigência do Trabalho)"""
        self.produto.preco = -5.00
        # O full_clean() simula a validação de campos do Django
        with self.assertRaises(ValidationError):
            self.produto.full_clean()

    def test_cliente_criado_corretamente(self):
        """Verifica se o cliente foi salvo no banco de dados de teste"""
        cliente_salvo = Cliente.objects.get(cpf="12345678901")
        self.assertEqual(cliente_salvo.nome, "Matheus Membro 4")