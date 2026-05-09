from django.contrib import admin
from .models import Cliente
from .models import Produto
from .models import Venda

admin.site.register(Cliente)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'quantidade_estoque')


admin.site.register(Venda)