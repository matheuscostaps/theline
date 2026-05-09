from django.db import models
from django.db import transaction
from clientes.models import Cliente
from produtos.models import Produto
from vendas.exceptions import EstoqueInsuficiente

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