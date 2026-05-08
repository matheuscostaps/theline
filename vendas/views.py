from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count
from django.db import transaction # Garante que se algo der errado, nada seja salvo

from .models import Venda
from .serializers import VendaSerializer
from clientes.models import Cliente
from produtos.models import Produto
from clientes.serializers import ClienteSerializer
from produtos.serializers import ProdutoSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

    def create(self, request, *args, **kwargs):
        itens = request.data.get('itens', [])
        if not itens:
            return Response({"error": "Não permitir venda sem itens"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                response = super().create(request, *args, **kwargs)
                return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def relatorio(self, request):
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        cliente_id = request.query_params.get('cliente_id')

        vendas_filtradas = Venda.objects.all()

        if data_inicio and data_fim:
            vendas_filtradas = vendas_filtradas.filter(data__range=[data_inicio, data_fim])
        
        if cliente_id:
            vendas_filtradas = vendas_filtradas.filter(cliente_id=cliente_id)

        dados_banco = vendas_filtradas.aggregate(
            faturamento_total=Sum('valor_total'),
            ticket_medio=Avg('valor_total'),
            total_vendas=Count('id')
        )

        return Response({
            "status": "sucesso",
            "indicadores": {
                "faturamento_total": dados_banco['faturamento_total'] or 0,
                "ticket_medio": dados_banco['ticket_medio'] or 0,
                "quantidade_vendas": dados_banco['total_vendas'],
            },
            "vendas": VendaSerializer(vendas_filtradas, many=True).data,
            "mensagem": "Relatório filtrado com sucesso"
        })