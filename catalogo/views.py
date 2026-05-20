from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Brinquedo
from .serializers import CategoriaSerializer, BrinquedoSerializer

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