from rest_framework import serializers
from .models import Cliente, Venda, ItemVenda, Produto


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'descricao','quantidade_estoque']



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
        read_only_fields = ['valor_total']
        
    def create(self, validated_data):
        itens_data = validated_data.pop('itens')

        # Cria a venda
        venda = Venda.objects.create(**validated_data)
        
        
        # Percorre os itens da venda
        for item_data in itens_data:
            produto = item_data['produto']
            quantidade = item_data['quantidade']

            # Verifica estoque
            if produto.quantidade_estoque < quantidade:
                raise serializers.ValidationError(
                    f"Estoque insuficiente para o produto "
                    f"{produto.nome}. Disponível: "
                    f"{produto.quantidade_estoque}"
                )

            # Cria o item da venda
            ItemVenda.objects.create(venda=venda, **item_data)

        # Retorna a venda criada
        return venda