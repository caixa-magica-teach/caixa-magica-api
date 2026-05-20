from rest_framework import serializers
from .models import Categoria, Brinquedo

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class BrinquedoSerializer(serializers.ModelSerializer):
    # Essa configuração permite que ao listar um brinquedo,
    # ele traga o objeto Categoria completo (nome, id) e não apenas o número do ID.
    categoria = CategoriaSerializer(read_only=True)

    # Mas quando formos criar (POST), passamos apenas o ID da categoria
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True
    )

    class Meta:
        model = Brinquedo
        fields = '__all__'
