from rest_framework import viewsets
from .models import Categoria, Brinquedo
from .serializers import CategoriaSerializer, BrinquedoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class BrinqueroViewSet(viewsets.ModelViewSet):
    queryset = Brinquedo.objects.all()
    serializer_class = BrinquedoSerializer