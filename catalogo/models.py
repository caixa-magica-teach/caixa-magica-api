from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Brinquedo(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('alugado', 'Alugado'),
        ('manutencao', 'Em Manutenção')
    ]

    nome = models.CharField(max_length=200)
    descricao_curta = models.CharField(max_length=255)
    descricao_completa = models.CharField()
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código Identificador')

    # Relacionamento 1:N com Categoria
    categoria = models.ForeignKey(Categoria, related_name='brinquedos', on_delete=models.SET_NULL, null=True)
    preco_diaria = models.DecimalField(max_digits=8, decimal_places=2)
    imagem_url = models.URLField(max_length=500, blank=True, null=True)
    status_atual = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    idade_recomendada = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome
    