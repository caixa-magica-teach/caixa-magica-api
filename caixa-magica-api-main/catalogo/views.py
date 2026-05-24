from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import exception_handler
from rest_framework.response import Response
from .models import Categoria, Brinquedo, Pedido, Cliente
from .serializers import CategoriaSerializer, BrinquedoSerializer, PedidoSerializer, ClienteSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class BrinquedoViewSet(viewsets.ModelViewSet):
    queryset = Brinquedo.objects.all()
    serializer_class = BrinquedoSerializer

    # 1. Adicionamos os "Motores" de busca e filtro
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    # 2. Quais campos aceitam filtro EXATO (ex: ?categoria=1 ou ?status_atual=disponivel)
    filterset_fields = ['categoria', 'status_atual']
    
    # 3. Quais campos aceitam busca por TEXTO PARCIAL (ex: ?search=Lego ou ?search=CM243)
    search_fields = ['nome', 'descricao_curta', 'codigo']

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "status": response.status_code,
            "mensagem": "Erro na requisição",
            "detalhes": response.data
        }
    return response