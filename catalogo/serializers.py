from rest_framework import serializers
from .models import Categoria, Brinquedo, ImagemBrinquedo

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ImagemBrinquedoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemBrinquedo
        # Retornamos apenas os dados úteis para o frontend montar o carrossel. 
        # Não precisamos retornar o ID do brinquedo aqui, pois já estará dentro dele.
        fields = ['id', 'imagem_url', 'ordem']

class BrinquedoSerializer(serializers.ModelSerializer):
    # Essa configuração permite que ao listar um brinquedo,
    # ele traga o objeto Categoria completo (nome, id) e não apenas o número do ID.
    categoria = CategoriaSerializer(read_only=True)

    # Mas quando formos criar (POST), passamos apenas o ID da categoria
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True
    )

    # PUXAMOS AS IMAGENS USANDO O RELATED_NAME
    # O nome da variável TEM que ser igual ao related_name='imagens' que você colocou no models.py
    imagens = ImagemBrinquedoSerializer(many=True)

    class Meta:
        model = Brinquedo
        fields = '__all__'

    # Sobrescrevemos o método de criação para lidar com as imagens
    def create(self, validated_data):
        # 1. Tiramos a lista de imagens dos dados validados antes de salvar o brinquedo
        imagens_data = validated_data.pop('imagens', [])
        
        # 2. Criamos o brinquedo no banco de dados
        brinquedo = Brinquedo.objects.create(**validated_data)
        
        # 3. Fazemos um loop na lista de imagens e criamos uma por uma, vinculando ao brinquedo
        for imagem_data in imagens_data:
            ImagemBrinquedo.objects.create(brinquedo=brinquedo, **imagem_data)
            
        return brinquedo
    
    # Sobrescrevemos o método de atualização para lidar com as imagens
    def update(self, instance, validated_data):
        # 1. Tiramos as imagens dos dados validados (usamos None como padrão para saber se foram enviadas)
        imagens_data = validated_data.pop('imagens', None)
        
        # 2. Atualizamos os campos normais do Brinquedo (nome, valor, status, etc.)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 3. Só mexemos nas imagens se o React as enviou no JSON
        if imagens_data is not None:
            # Apaga as imagens antigas do banco
            instance.imagens.all().delete()
            
            # Recria as imagens com os dados novos vindos do PUT
            for imagem_data in imagens_data:
                ImagemBrinquedo.objects.create(brinquedo=instance, **imagem_data)
                
        return instance