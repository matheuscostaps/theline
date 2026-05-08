from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count

from .models import Venda
from .serializers import VendaSerializer
from clientes.models import Cliente
from produtos.models import Produto
from clientes.serializers import ClienteSerializer
from produtos.serializers import ProdutoSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

    @action(detail=False, methods=['get'])
    def relatorio(self, request):
        # Agregações de Vendas
        dados_banco = Venda.objects.aggregate(
            faturamento_total=Sum('valor_total'),
            ticket_medio=Avg('valor_total'),
            total_vendas=Count('id')
        )

        # Busca todos os clientes e produtos
        clientes = Cliente.objects.all()
        produtos = Produto.objects.all()
        vendas_detalhadas = Venda.objects.all()

        return Response({
            "status": "sucesso",
            "indicadores": {
                "faturamento_total": dados_banco['faturamento_total'] or 0,
                "ticket_medio": dados_banco['ticket_medio'] or 0,
                "quantidade_vendas": dados_banco['total_vendas'],
            },
            "clientes": ClienteSerializer(clientes, many=True).data,
            "produtos": ProdutoSerializer(produtos, many=True).data,
            "vendas": VendaSerializer(vendas_detalhadas, many=True).data,
            "mensagem": "Relatório consolidado extraído com sucesso"
        })