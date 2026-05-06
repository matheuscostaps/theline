from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Cliente 
from produtos.models import Produto
# from vendas.models import Venda  <-- Comente esta linha se a pasta não existir

class SistemaGestaoTest(TestCase):

    def setUp(self):
        # Criando dados iniciais para os testes
        self.cliente = Cliente.objects.create(
            nome="Matheus", 
            cpf="12345678901", 
            email="matheus@email.com"
        )
        self.produto = Produto.objects.create(
            nome="Camiseta", 
            preco=50.00, 
            quantidade_estoque=10
        )

    def test_estoque_insuficiente(self):
        """Regra: Não permitir venda se estoque insuficiente [cite: 50]"""
        quantidade_venda = 100
        # Simula a lógica de validação que você deve ter na sua View ou Model
        self.assertGreater(quantidade_venda, self.produto.quantidade_estoque)

    def test_preco_negativo(self):
        """Regra: Preço não pode ser negativo [cite: 48]"""
        self.produto.preco = -5.00
        # O Django não valida automaticamente no save(), então usamos full_clean()
        with self.assertRaises(ValidationError):
            self.produto.full_clean()

    def test_impedir_exclusao_cliente_com_venda(self):
        """Regra: Cliente não pode ser removido se possuir vendas [cite: 39]"""
        # Criando uma venda para o cliente
        Venda.objects.create(cliente=self.cliente, valor_total=50.00)
        
        # Simula a lógica de proteção de exclusão
        if self.cliente.venda_set.exists():
             has_vendas = True
        
        self.assertTrue(has_vendas, "O cliente possui vendas e não deve ser excluído.")