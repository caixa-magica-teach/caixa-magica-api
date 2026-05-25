from django.db import models
from django.contrib.auth.models import User

# 1. CLIENTE
class Cliente(models.Model):
    # O OneToOneField conecta a tabela nativa do Django (que já tem email e senha) 
    # com os dados extras exigidos pela LGPD no PDF.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
    telefone = models.CharField(max_length=20)
    endereco_padrao = models.TextField(help_text="Endereço principal para entrega")

    def __str__(self):
        # Retorna o nome completo se existir, senão o username
        return self.user.get_full_name() or self.user.username


# 2. CATEGORIA
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


# 3. BRINQUEDO
class Brinquedo(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('alugado', 'Alugado'),
        ('manutencao', 'Em Manutenção')
    ]

    nome = models.CharField(max_length=200)
    descricao_curta = models.CharField(max_length=255)
    descricao_completa = models.TextField() # Corrigido para TextField
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código Identificador')
    categoria = models.ForeignKey(Categoria, related_name='brinquedos', on_delete=models.SET_NULL, null=True)
    
    # Adaptado de preco_diaria para valor_base para facilitar o cálculo dos blocos de 7, 15 e 30 dias
    valor_base = models.DecimalField(max_digits=8, decimal_places=2)
    regras_aluguel = models.TextField(blank=True, null=True, help_text="Ex: Devolver limpo, não usar na terra.")
    status_atual = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    idade_recomendada = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome

# 4 TABELA PARA SUPORTAR MÚLTIPLAS IMAGENS
class ImagemBrinquedo(models.Model):
    # O CASCADE garante que, se o brinquedo for deletado, todas as fotos dele também serão
    brinquedo = models.ForeignKey(Brinquedo, related_name='imagens', on_delete=models.CASCADE)
    
    # Mantemos como URLField para facilitar esse MVP, sem precisar configurar servidores de arquivos agora
    imagem_url = models.URLField(max_length=500)
    
    # Campo crucial para o carrossel: define qual foto aparece primeiro
    ordem = models.PositiveIntegerField(default=0, help_text="0 será a foto principal da capa, 1 em diante no carrossel")

    class Meta:
        # Garante que o banco de dados sempre entregue as fotos na ordem correta
        ordering = ['ordem']

    def __str__(self):
        return f"Foto {self.ordem} - {self.brinquedo.nome}"

# 5. PEDIDO
class Pedido(models.Model):
    PRAZO_CHOICES = [
        (7, '7 Dias'),
        (15, '15 Dias'),
        (30, '30 Dias'),
    ]
    
    LOGISTICA_CHOICES = [
        ('entrega', 'Entrega'),
        ('retirada', 'Retirada'),
    ]

    STATUS_PEDIDO_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('em_andamento', 'Em Andamento (Alugado)'),
        ('concluido', 'Concluído / Devolvido'),
        ('cancelado', 'Cancelado'),
    ]

    # PROTECT impede que um cliente seja deletado do banco se ele tiver pedidos atrelados
    cliente = models.ForeignKey(Cliente, related_name='pedidos', on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)
    prazo_aluguel = models.IntegerField(choices=PRAZO_CHOICES)
    tipo_logistica = models.CharField(max_length=20, choices=LOGISTICA_CHOICES)
    endereco_entrega = models.TextField(blank=True, null=True, help_text="Preencher se for entrega")
    status_aluguel = models.CharField(max_length=20, choices=STATUS_PEDIDO_CHOICES, default='pendente')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.user.username}"


# 6. ITEM DO PEDIDO (Tabela intermediária N:M)
class ItemPedido(models.Model):
    # Conecta os brinquedos ao pedido final
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    brinquedo = models.ForeignKey(Brinquedo, related_name='historico_pedidos', on_delete=models.PROTECT)
    
    # Grava o preço que o usuário pagou no dia. 
    # Se o 'valor_base' do brinquedo subir amanhã, o histórico desse pedido não é alterado.
    preco_no_momento = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.brinquedo.nome} (Pedido #{self.pedido.id})"