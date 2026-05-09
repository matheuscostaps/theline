from rest_framework import serializers
from .models import Cliente
from .models import Venda, ItemVenda
from .models import Produto

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'quantidade_estoque']

class ItemVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVenda
        fields = '__all__'
        read_only_fields = ['venda']

class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True)

    class Meta:
        model = Venda
        fields = '__all__'

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        venda = Venda.objects.create(**validated_data)
        
        for item_data in itens_data:
            produto = item_data['produto']
            quantidade = item_data['quantidade']

            if produto.quantidade_estoque < quantidade:
                raise serializers.ValidationError(
                    f"Estoque insuficiente para o produto {produto.nome}. Disponível: {produto.quantidade_estoque}"
                )
            
            ItemVenda.objects.create(venda=venda, **item_data)
            
            produto.quantidade_estoque -= quantidade

            produto.save()  
            return venda