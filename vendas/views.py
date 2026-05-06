from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count # Ferramentas de banco de dados
from .models import Venda
from .serializers import VendaSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

    @action(detail=False, methods=['get'])
    def relatorio(self, request):
        # 1. Puxa a soma total da coluna 'valor_total' do banco
        dados_banco = Venda.objects.aggregate(
            faturamento_total=Sum('valor_total'),
            ticket_medio=Avg('valor_total'),
            total_vendas=Count('id')
        )

        return Response({
            "status": "sucesso",
            "faturamento_total": dados_banco['faturamento_total'] or 0,
            "ticket_medio": dados_banco['ticket_medio'] or 0,
            "quantidade_vendas": dados_banco['total_vendas'],
            "mensagem": "Dados extraídos em tempo real do banco de dados"
        })