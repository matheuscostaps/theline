from django.db import models
from django.db import transaction
from django.core.exceptions import ValidationError
from .exceptions import EstoqueInsuficiente

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome
    
# Função de validação para o preço
def validar_preco_positivo(valor):
    if valor < 0:
        raise ValidationError("O preço não pode ser negativo.")

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    # Adicionamos o validator aqui
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_preco_positivo])
    quantidade_estoque = models.IntegerField(default=0)

    def baixar_estoque(self, quantidade):
        if self.quantidade_estoque < quantidade:
            raise ValidationError(f"Estoque insuficiente para o produto {self.nome}.")
        
        self.quantidade_estoque -= quantidade
        self.save()

    def __str__(self):
        return self.nome

class Venda(models.Model):
    data_venda = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='vendas')

    def __str__(self):
        return f"Venda {self.id} - Cliente: {self.cliente.nome}"
    
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x Produto {self.produto_id} (Venda {self.venda.id})"
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.pk: 
                produto = self.produto
                if produto.quantidade_estoque < self.quantidade:
                    raise EstoqueInsuficiente()
                
                produto.quantidade_estoque -= self.quantidade
                produto.save()
            
            super().save(*args, **kwargs)