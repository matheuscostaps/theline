from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg, Count
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib import messages # Adicione isso no topo!
from .models import Cliente, Produto, Venda, ItemVenda
# Importe seus modelos e serializers
from .models import Cliente, Produto, Venda
from .serializers import ClienteSerializer, ProdutoSerializer, VendaSerializer
from django.db.models import ProtectedError


# ==========================================
# VIEWS DE FRONTEND (Páginas HTML)
# ==========================================

def dashboard_view(request):
    return render(request, 'web/index.html')

def produtos_view(request):
    return render(request, 'web/produtos.html')

def vendas_view(request):
    return render(request, 'web/vendas.html')

# --- CRUD Clientes (Sem JavaScript) ---

def clientes_view(request):
    clientes = Cliente.objects.all()
    cliente_edit = None
    
    id_editar = request.GET.get('editar')
    if id_editar:
        cliente_edit = get_object_or_404(Cliente, id=id_editar)
        
    return render(request, 'web/clientes.html', {
        'clientes': clientes,
        'cliente_edit': cliente_edit
    })

def criar_cliente(request):
    if request.method == "POST":
        Cliente.objects.create(
            nome=request.POST.get('nome'),
            cpf=request.POST.get('cpf'),
            email=request.POST.get('email'),
            telefone=request.POST.get('telefone'),
            endereco=request.POST.get('endereco'),
        )
    return redirect('clientes')

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.nome = request.POST.get('nome')
        cliente.cpf = request.POST.get('cpf')
        cliente.email = request.POST.get('email')
        cliente.telefone = request.POST.get('telefone')
        cliente.endereco = request.POST.get('endereco')
        cliente.save()
    return redirect('clientes')

def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
    return redirect('clientes')

# --- Lógica do CRUD de Produtos (Sem JavaScript) ---

def produtos_view(request):
    produtos = Produto.objects.all()
    produto_edit = None
    
    # Se a URL tiver ?editar=ID, busca o produto para preencher o form
    id_editar = request.GET.get('editar')
    if id_editar:
        produto_edit = get_object_or_404(Produto, id=id_editar)
        
    return render(request, 'web/produtos.html', {
        'produtos': produtos,
        'produto_edit': produto_edit
    })

def criar_produto(request):
    if request.method == "POST":
        # A regra do PDF diz que o preço não pode ser negativo. Você pode validar isso depois no banco ou forms!
        Produto.objects.create(
            nome=request.POST.get('nome'),
            descricao=request.POST.get('descricao', ''),
            preco=request.POST.get('preco'),
            quantidade_estoque=request.POST.get('quantidade_estoque'),
        )
    return redirect('produtos')

def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == "POST":
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao', '')
        produto.preco = request.POST.get('preco')
        produto.quantidade_estoque = request.POST.get('quantidade_estoque')
        produto.save()
    return redirect('produtos')

def excluir_produto(request, pk):
    # Busca o produto ou retorna 404 se não existir
    produto = get_object_or_404(Produto, pk=pk)
    
    if request.method == 'POST':
        try:
            produto.delete()
            messages.success(request, "Produto excluído com sucesso!")
        except ProtectedError:
            # Esta é a parte que resolve o seu erro:
            messages.error(request, f"Não é possível excluir '{produto.nome}' pois ele está vinculado a uma venda já realizada.")
        
        return redirect('produtos')
    
    # Se alguém tentar acessar via GET, apenas redireciona
    return redirect('produtos')

def vendas_view(request):
    vendas = Venda.objects.all().order_by('-id')
    clientes = Cliente.objects.all() # Precisamos dos clientes para o select da nova venda
    return render(request, 'web/vendas.html', {
        'vendas': vendas,
        'clientes': clientes
    })

def criar_venda(request):
    if request.method == "POST":
        cliente_id = request.POST.get('cliente_id')
        cliente = get_object_or_404(Cliente, id=cliente_id)
        
        # Cria a venda zerada
        venda = Venda.objects.create(cliente=cliente, valor_total=0)
        
        # Redireciona para a tela de adicionar produtos nela
        return redirect('detalhes_venda', pk=venda.id)
    return redirect('vendas')

def detalhes_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    itens = ItemVenda.objects.filter(venda=venda)
    produtos = Produto.objects.filter(quantidade_estoque__gt=0) # Só mostra produtos que tem estoque > 0
    
    return render(request, 'web/detalhes_venda.html', {
        'venda': venda,
        'itens': itens,
        'produtos': produtos
    })



def adicionar_item_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    
    if request.method == "POST":
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade', 1))
        produto = get_object_or_404(Produto, id=produto_id)

        if produto.quantidade_estoque >= quantidade:
            # CORREÇÃO AQUI: Passando o preco_unitario do produto
            ItemVenda.objects.create(
                venda=venda, 
                produto=produto, 
                quantidade=quantidade,
                preco_unitario=produto.preco  # <--- Adicione esta linha
            )
            
            # Atualiza estoque
            produto.quantidade_estoque -= quantidade
            produto.save()

            # Recalcula total da venda
            total = sum((item.preco_unitario * item.quantidade) for item in ItemVenda.objects.filter(venda=venda))
            venda.valor_total = total
            venda.save()
        else:
            messages.error(request, f"Estoque insuficiente para {produto.nome}.")

    return redirect('detalhes_venda', pk=venda.id)

def relatorios_view(request):
    # CORREÇÃO AQUI: mudado de '-data' para '-data_venda'
    vendas = Venda.objects.all().order_by('-data_venda') 
    clientes = Cliente.objects.all()

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if data_inicio and data_fim:
        # CORREÇÃO AQUI: mudado de 'data__range' para 'data_venda__range'
        vendas = vendas.filter(data_venda__range=[data_inicio, data_fim])

    cliente_id = request.GET.get('cliente_id')
    if cliente_id:
        vendas = vendas.filter(cliente_id=cliente_id)

    total_geral = sum(venda.valor_total for venda in vendas)

    return render(request, 'web/relatorios.html', {
        'vendas': vendas,
        'clientes': clientes,
        'total_geral': total_geral,
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'cliente_id': cliente_id,
        }
    })
# ==========================================
# VIEWS DA API (DRF)
# ==========================================

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