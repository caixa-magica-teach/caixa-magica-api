from rest_framework import serializers
from datetime import date
from django.contrib.auth.models import User
from .models import Categoria, Brinquedo, ImagemBrinquedo, Pedido, Cliente
from datetime import date
from django.contrib.auth.models import User
from .models import Categoria, Brinquedo, ImagemBrinquedo, Pedido, Cliente

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ImagemBrinquedoSerializer(serializers.ModelSerializer):

    brinquedo = serializers.PrimaryKeyRelatedField(
        queryset=Brinquedo.objects.all(), 
        required=False
    )

    class Meta:
        model = ImagemBrinquedo
        fields = ['id', 'brinquedo', 'imagem_url', 'ordem']

class BrinquedoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True
    )
    imagens = ImagemBrinquedoSerializer(many=True)

    class Meta:
        model = Brinquedo
        fields = '__all__'

    def create(self, validated_data):
        imagens_data = validated_data.pop('imagens', [])
        brinquedo = Brinquedo.objects.create(**validated_data)
        for imagem_data in imagens_data:
            ImagemBrinquedo.objects.create(brinquedo=brinquedo, **imagem_data)
        return brinquedo
    
    def update(self, instance, validated_data):
        imagens_data = validated_data.pop('imagens', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if imagens_data is not None:
            instance.imagens.all().delete()
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

    def validate(self, data):
        valor_total = data.get('valor_total', 0)
        if valor_total < 0:
            raise serializers.ValidationError(
                {"valor_total": "O valor total do pedido não pode ser negativo!"}
            )
        return data

class ClienteSerializer(serializers.ModelSerializer):
    # Campos extras para receber os dados do User vindos do React
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Cliente
        fields = ['id', 'user', 'username', 'email', 'password', 'first_name', 'telefone', 'endereco_padrao']
        read_only_fields = ['user']

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name', '')

        # 1. Cria o usuário do Django com a senha criptografada
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name
        )

        # 2. Cria o Cliente vinculando ao User criado
        cliente = Cliente.objects.create(user=user, **validated_data)
        return cliente

    # Validação LGPD para o Telefone
    def validate_telefone(self, value):
        telefone_limpo = ''.join(filter(str.isdigit, value))
        if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
            raise serializers.ValidationError(
                "O telefone deve conter o DDD e ter entre 10 e 11 dígitos numéricos."
            )
        return value

    # Validação LGPD para o Endereço
    def validate_endereco_padrao(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "O endereço de entrega fornecido está incompleto."
            )
        return value

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

    def validate(self, data):
        valor_total = data.get('valor_total', 0)
        if valor_total < 0:
            raise serializers.ValidationError(
                {"valor_total": "O valor total do pedido não pode ser negativo!"}
            )
        return data

class ClienteSerializer(serializers.ModelSerializer):
    # Campos extras para receber os dados do User vindos do React
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Cliente
        fields = ['id', 'user', 'username', 'email', 'password', 'first_name', 'telefone', 'endereco_padrao']
        read_only_fields = ['user']

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name', '')

        # 1. Cria o usuário do Django com a senha criptografada
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name
        )

        # 2. Cria o Cliente vinculando ao User criado
        cliente = Cliente.objects.create(user=user, **validated_data)
        return cliente

    # Validação LGPD para o Telefone
    def validate_telefone(self, value):
        telefone_limpo = ''.join(filter(str.isdigit, value))
        if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
            raise serializers.ValidationError(
                "O telefone deve conter o DDD e ter entre 10 e 11 dígitos numéricos."
            )
        return value

    # Validação LGPD para o Endereço
    def validate_endereco_padrao(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "O endereço de entrega fornecido está incompleto."
            )
        return value