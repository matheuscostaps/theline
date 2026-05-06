from django.db import models
from django.core.validators import MinValueValidator # Importe isso!

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    # Adicione o validator aqui:
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)] 
    )
    quantidade_estoque = models.IntegerField(default=0)

    def baixar_estoque(self, quantidade):
        if self.quantidade_estoque < quantidade:
            raise ValidationError(f"Estoque insuficiente para o produto {self.nome}.")
        
        self.quantidade_estoque -= quantidade
        self.save()

    def __str__(self):
        return self.nome