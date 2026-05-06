from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Produto
from .serializers import ProdutoSerializer

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