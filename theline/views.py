from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg, Count
from django.db import transaction
from django.db.models import ProtectedError
from django.contrib import messages

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cliente, Produto, Venda, ItemVenda
from .serializers import ClienteSerializer, ProdutoSerializer, VendaSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ClienteForm, ProdutoForm

from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q

# ==========================================
# VIEWS DE FRONTEND (Páginas HTML)
# ==========================================

# --- CRUD Clientes ---

@login_required(login_url='login')
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

@login_required(login_url='login')
def criar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()

    return redirect('clientes')

@login_required(login_url='login')
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        form = ClienteForm(
            request.POST,
            instance=cliente
        )

        if form.is_valid():
            form.save()

    return redirect('clientes')

@login_required(login_url='login')
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, "Cliente excluído com sucesso!")

        except ProtectedError:
            messages.error(
                request,
                f"Não é possível excluir o cliente '{cliente.nome}' porque ele possui vendas registradas."
            )

    return redirect('clientes')


# --- CRUD Produtos ---

@login_required(login_url='login')
def produtos_view(request):
    produtos = Produto.objects.all()
    produto_edit = None

    id_editar = request.GET.get('editar')

    if id_editar:
        produto_edit = get_object_or_404(Produto, id=id_editar)

    return render(request, 'web/produtos.html', {
        'produtos': produtos,
        'produto_edit': produto_edit
    })

@login_required(login_url='login')
def criar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()

    return redirect('produtos')

@login_required(login_url='login')
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == "POST":
        form = ProdutoForm(
            request.POST,
            instance=produto
        )

        if form.is_valid():
            form.save()

    return redirect('produtos')

@login_required(login_url='login')
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        try:
            produto.delete()
            messages.success(request, "Produto excluído com sucesso!")

        except ProtectedError:
            messages.error(
                request,
                f"Não é possível excluir '{produto.nome}' pois ele está vinculado a uma venda já realizada."
            )

    return redirect('produtos')


# --- CRUD Vendas ---

@login_required(login_url='login')
def vendas_view(request):
    vendas = Venda.objects.all().order_by('-id')
    clientes = Cliente.objects.all()

    return render(request, 'web/vendas.html', {
        'vendas': vendas,
        'clientes': clientes
    })

@login_required(login_url='login')
def criar_venda(request):
    if request.method == "POST":
        cliente_id = request.POST.get('cliente_id')
        cliente = get_object_or_404(Cliente, id=cliente_id)

        venda = Venda.objects.create(
            cliente=cliente,
            valor_total=0
        )

        return redirect('detalhes_venda', pk=venda.id)

    return redirect('vendas')

@login_required(login_url='login')
def detalhes_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)

    itens = ItemVenda.objects.filter(venda=venda)

    produtos = Produto.objects.filter(
        quantidade_estoque__gt=0
    )

    return render(request, 'web/detalhes_venda.html', {
        'venda': venda,
        'itens': itens,
        'produtos': produtos
    })

@login_required(login_url='login')
def adicionar_item_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)

    if request.method == "POST":
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade', 1))

        produto = get_object_or_404(Produto, id=produto_id)

        if produto.quantidade_estoque >= quantidade:

            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco
            )

            # Atualiza estoque
            produto.quantidade_estoque -= quantidade
            produto.save()

            # Atualiza total da venda
            total = sum(
                item.preco_unitario * item.quantidade
                for item in ItemVenda.objects.filter(venda=venda)
            )

            venda.valor_total = total
            venda.save()

        else:
            messages.error(
                request,
                f"Estoque insuficiente para {produto.nome}."
            )

    return redirect('detalhes_venda', pk=venda.id)


# --- Relatórios ---

@login_required(login_url='login')
def relatorios_view(request):
    vendas = Venda.objects.all().order_by('-data_venda')
    clientes = Cliente.objects.all()

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if data_inicio and data_fim:
        vendas = vendas.filter(
            data_venda__range=[data_inicio, data_fim]
        )

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

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def baixar_estoque(self, request, pk=None):
        produto = self.get_object()

        quantidade = request.data.get('quantidade', 0)

        try:
            produto.baixar_estoque(int(quantidade))

            return Response(
                {'status': 'estoque atualizado'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        itens = request.data.get('itens', [])

        if not itens:
            return Response(
                {"error": "Não permitir venda sem itens"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                response = super().create(request, *args, **kwargs)
                return response

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def relatorio(self, request):

        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        cliente_id = request.query_params.get('cliente_id')

        vendas_filtradas = Venda.objects.all()

        if data_inicio and data_fim:
            vendas_filtradas = vendas_filtradas.filter(
                data_venda__range=[data_inicio, data_fim]
            )

        if cliente_id:
            vendas_filtradas = vendas_filtradas.filter(
                cliente_id=cliente_id
            )

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
            "vendas": VendaSerializer(
                vendas_filtradas,
                many=True
            ).data,
            "mensagem": "Relatório filtrado com sucesso"
        })

# ==========================================
# PÁGINA DE REGISTRO
# ==========================================

def register_view(request):
  if request.method == "POST":
    # Valores informados no cadastro
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    if password == confirm_password:
      # Inclusão no banco de dados do novo usuário
      user = User.objects.create_user(username=username, password=password)
      messages.success(request, "Usuário criado com sucesso!")
      return redirect('login')
    else:
      messages.error(request, "As senhas não conferem!")

  return render(request, 'web/register.html')

# ==========================================
# PÁGINA DE LOGIN
# ==========================================

def login_view(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    # Método para verificar as credenciais
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user) # cria a sessão
      return redirect('dashboard')
    else:
      messages.error(request, "Usuário ou senha inválidos!")
  return render(request, 'web/login.html')

# ==========================================
# PÁGINA DE LOGOUT
# ==========================================

def logout_view(request):
  logout(request)
  return redirect('login')

# Dashboard protegido
@login_required(login_url='login')
def dashboard(request):
  
  return render(request, 'web/index.html')

# ==========================================
# BUSCA DINAMICA
# ==========================================

def busca_global(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'results': []})

    results = []
    query_lower = query.lower()

    if 'prod' in query_lower:
        results.append({
            'categoria': 'Páginas',
            'texto': 'Gerenciar Produtos',
            'url': reverse('produtos')
        })
    if 'cli' in query_lower:
        results.append({
            'categoria': 'Páginas',
            'texto': 'Gerenciar Clientes',
            'url': reverse('clientes')
        })
    if 'vend' in query_lower:
        results.append({
            'categoria': 'Páginas',
            'texto': 'Histórico de Vendas',
            'url': reverse('vendas')
        })
    
    produtos = Produto.objects.filter(nome__icontains=query)[:4]
    for p in produtos:
        results.append({
            'categoria': 'Produtos',
            'texto': f"{p.nome} (R$ {p.preco})",
            'url': reverse('produtos') + f"?busca={p.id}"
        })

    clientes = Cliente.objects.filter(
        Q(nome__icontains=query) | 
        Q(email__icontains=query) | 
        Q(telefone__icontains=query) | 
        Q(endereco__icontains=query)
    )[:4]

    for c in clientes:
        texto_exibicao = c.nome
        
        if c.nome and query_lower in c.nome.lower():
            texto_exibicao = c.nome
        elif c.email and query_lower in c.email.lower():
            texto_exibicao = c.email
        elif c.telefone and query_lower in str(c.telefone).lower():
            texto_exibicao = str(c.telefone)
        elif c.endereco and query_lower in c.endereco.lower():
            texto_exibicao = c.endereco

        results.append({
            'categoria': 'Clientes',
            'texto': texto_exibicao,
            'url': reverse('clientes') + f"?busca={c.id}" 
        })

    return JsonResponse({'results': results})
