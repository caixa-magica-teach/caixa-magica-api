from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import exception_handler
from rest_framework.response import Response

# 1. ADICIONE O ImagemBrinquedo NO IMPORT DOS MODELS:
from .models import Categoria, Brinquedo, Pedido, Cliente, ImagemBrinquedo 

from .serializers import (
    CategoriaSerializer, 
    BrinquedoSerializer, 
    PedidoSerializer, 
    ClienteSerializer, 
    ImagemBrinquedoSerializer
)

class ImagemBrinquedoViewSet(viewsets.ModelViewSet):
    queryset = ImagemBrinquedo.objects.all()
    serializer_class = ImagemBrinquedoSerializer
    
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class BrinquedoViewSet(viewsets.ModelViewSet):
    queryset = Brinquedo.objects.all()
    serializer_class = BrinquedoSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria', 'status_atual']
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