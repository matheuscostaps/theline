from django.db import models
from django.core.exceptions import ValidationError

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