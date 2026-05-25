from rest_framework import serializers
from datetime import date
from .models import Categoria, Brinquedo, ImagemBrinquedo, Pedido, Cliente

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

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'id', 
            'cliente', 
            'prazo_aluguel', 
            'tipo_logistica', 
            'endereco_entrega', 
            'status_aluguel', 
            'valor_total', 
            'data_criacao'
        ]

    # Função para manter a consistência do valor
    def validate(self, data):
        # Buscamos o valor_total de forma segura. Se ele não vier, assume 0
        valor_total = data.get('valor_total', 0)

        # Bloqueia valores negativos
        if valor_total < 0:
            raise serializers.ValidationError(
                {"valor_total": "O valor total do pedido não pode ser negativo!"}
            )

        # Retorna os dados limpos se estiver tudo certo
        return data
    
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        # Coleta mínima: apenas o estritamente necessário para o funcionamento do sistema
        fields = ['id', 'user', 'telefone', 'endereco_padrao']

    # Validação LGPD para o Telefone
    def validate_telefone(self, value):
        # Remove espaços, parênteses e traços para testar apenas os números
        telefone_limpo = ''.join(filter(str.isdigit, value))
        
        # Valida se tem o DDD + número (10 para fixo ou 11 para celular)
        if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
            raise serializers.ValidationError(
                "O telefone deve conter o DDD e ter entre 10 e 11 dígitos numéricos."
            )
        return value

    # Validação LGPD para o Endereço
    def validate_endereco_padrao(self, value):
        # Remove espaços extras e checa se o endereço está muito curto/incompleto
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "O endereço de entrega fornecido está incompleto."
            )
        return value