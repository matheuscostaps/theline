from .models import Produto, Venda
from rest_framework.decorators import action
from .models import Cliente
from .serializers import ClienteSerializer, ProdutoSerializer, VendaSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Produto
from .serializers import ProdutoSerializer
from django.db.models import Sum, Avg, Count
from django.db import transaction
from django.shortcuts import render

# Views de frontend (HTML)
def dashboard_view(request):
    return render(request, 'web/index.html')

def produtos_view(request):
    return render(request, 'web/produtos.html')

def vendas_view(request):
    return render(request, 'web/vendas.html')

def clientes_view(request):
    return render(request, 'clientes.html')


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    @action(detail=True, methods=['post'])
    def baixar_estoque(self, request, pk=None):
        produto = self.get_object()
        quantidade = request.data.get('quantidade', 0)

        try:
            produto.baixar_estoque(int(quantidade))
            return Response({'status': 'estoque atualizado'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    
