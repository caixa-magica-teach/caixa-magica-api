# 🎲 Caixa Mágica - API

> **Backend do sistema de aluguel de brinquedos Caixa Mágica**  
> API RESTful desenvolvida com Django REST Framework para gerenciamento de catálogo, clientes, pedidos e aluguéis de brinquedos.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Modelagem de Dados](#-modelagem-de-dados)
  - [Diagrama de Entidades](#diagrama-de-entidades)
  - [Modelos](#modelos)
- [Endpoints da API](#-endpoints-da-api)
  - [Categorias](#categorias)
  - [Brinquedos](#brinquedos)
  - [Pedidos](#pedidos)
  - [Clientes](#clientes)
  - [Autenticação JWT](#autenticação-jwt)
- [Como Executar](#-como-executar)
  - [Pré-requisitos](#pré-requisitos)
  - [Passo a passo](#passo-a-passo)
- [Exemplos de Uso](#-exemplos-de-uso)
  - [Criar um cliente](#1-criar-um-cliente)
  - [Obter token JWT](#2-obter-token-jwt)
  - [Listar brinquedos](#3-listar-brinquedos-com-filtros-e-busca)
  - [Criar um pedido](#4-criar-um-pedido)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Desenvolvimento](#-desenvolvimento)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

A **Caixa Mágica** é uma plataforma de aluguel de brinquedos que permite que clientes aluguem brinquedos por períodos de **7, 15 ou 30 dias**, com opções de **entrega** ou **retirada**.

Esta API foi construída seguindo boas práticas de desenvolvimento:

- ✅ **Versionamento de API** (`/api/v1/`) para facilitar evoluções futuras
- ✅ **Autenticação JWT** (JSON Web Token) para segurança das requisições
- ✅ **Filtros e busca** nos endpoints de brinquedos e categorias
- ✅ **Tratamento customizado de erros** com respostas padronizadas
- ✅ **Validações LGPD** para dados sensíveis (telefone, endereço)
- ✅ **Suporte a múltiplas imagens** por brinquedo com ordenação para carrossel
- ✅ **CORS configurado** para integração com frontends locais

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|-----------|--------|--------|
| [Python](https://www.python.org/) | 3.x | Linguagem de programação |
| [Django](https://www.djangoproject.com/) | 6.0.5 | Framework web |
| [Django REST Framework](https://www.django-rest-framework.org/) | - | Framework para construção de APIs REST |
| [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/) | - | Autenticação por JSON Web Token |
| [django-filter](https://django-filter.readthedocs.io/) | - | Filtros avançados para os endpoints |
| [django-cors-headers](https://github.com/adamchainz/django-cors-headers/) | - | Liberação de CORS para o frontend |
| [SQLite](https://www.sqlite.org/) | - | Banco de dados (desenvolvimento) |

---

## 🗄️ Modelagem de Dados

### Diagrama de Entidades

```
┌──────────────┐       ┌──────────────────┐        ┌──────────────────┐
│    User      │       │    Categoria     │        │   ImagemBrinquedo│
│ (Django Auth)│       │──────────────────│        │──────────────────│
│──────────────│       │ id (PK)          │        │ id (PK)          │
│ id (PK)      │       │ nome             │────────│ brinquedo (FK)   │
│ username     │       │ descricao        │    │   │ imagem_url       │
│ email        │       └──────────────────┘    │   │ ordem            │
│ password     │                               │   └──────────────────┘
└──────┬───────┘                               │
       │ 1:1                                   │
       │                                       │ N
┌──────┴────────────┐          ┌───────────────┴────────────┐
│     Cliente       │          │        Brinquedo           │
│───────────────────│          │────────────────────────────│
│ id (PK)           │          │ id (PK)                    │
│ user (FK - User)  │          │ nome                       │
│ telefone          │──────────│ descricao_curta            │
│ endereco_padrao   │    N     │ descricao_completa         │
└──────┬────────────┘          │ codigo (unique)            │
       │                       │ categoria (FK - Categoria) │
       │ 1:N                   │ valor_base                 │
       │                       │ regras_aluguel             │
       │                       │ status_atual               │
       │                       │ idade_recomendada          │
       │                       └────────────────────────────┘
       │                                    │
       │                                    │ N
       │                                    │
┌──────┴─────────────────┐      ┌───────────┴─────────────────┐
│        Pedido          │      │        ItemPedido           │
│────────────────────────│      │─────────────────────────────│
│ id (PK)                │      │ id (PK)                     │
│ cliente (FK - Cliente) │──────│ pedido (FK - Pedido)        │
│ data_criacao           │  N   │ brinquedo (FK - Brinquedo)  │
│ prazo_aluguel          │      │ preco_no_momento            │
│ tipo_logistica         │      └─────────────────────────────┘
│ endereco_entrega       │
│ status_aluguel         │
│ valor_total            │
└────────────────────────┘
```

### Modelos

#### 👤 Cliente
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `user` | `OneToOneField` → `User` | Usuário de autenticação do Django (nome, email, senha) |
| `telefone` | `CharField` (20) | Telefone com DDD (validado com 10-11 dígitos - LGPD) |
| `endereco_padrao` | `TextField` | Endereço principal para entrega (validado - LGPD) |

#### 🏷️ Categoria
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nome` | `CharField` (100) | Nome da categoria |
| `descricao` | `TextField` | Descrição da categoria (opcional) |

#### 🧸 Brinquedo
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nome` | `CharField` (200) | Nome do brinquedo |
| `descricao_curta` | `CharField` (255) | Breve descrição |
| `descricao_completa` | `TextField` | Descrição detalhada |
| `codigo` | `CharField` (50) | Código identificador único |
| `categoria` | `ForeignKey` → `Categoria` | Categoria do brinquedo |
| `valor_base` | `DecimalField` (8,2) | Valor base para cálculo dos blocos de locação |
| `regras_aluguel` | `TextField` | Regras do aluguel (ex: "Devolver limpo") |
| `status_atual` | `CharField` | Status: `disponivel`, `alugado` ou `manutencao` |
| `idade_recomendada` | `CharField` (50) | Faixa etária recomendada |

#### 📸 ImagemBrinquedo
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `brinquedo` | `ForeignKey` → `Brinquedo` | Brinquedo associado (CASCADE na deleção) |
| `imagem_url` | `URLField` (500) | URL da imagem |
| `ordem` | `PositiveIntegerField` | Ordem de exibição (0 = capa, 1+ = carrossel) |

#### 📦 Pedido
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `cliente` | `ForeignKey` → `Cliente` | Cliente que fez o pedido (PROTECT) |
| `data_criacao` | `DateTimeField` | Data de criação (automático) |
| `prazo_aluguel` | `IntegerField` | Prazo: `7`, `15` ou `30` dias |
| `tipo_logistica` | `CharField` | `entrega` ou `retirada` |
| `endereco_entrega` | `TextField` | Endereço de entrega (se aplicável) |
| `status_aluguel` | `CharField` | Status: `pendente`, `aprovado`, `em_andamento`, `concluido`, `cancelado` |
| `valor_total` | `DecimalField` (10,2) | Valor total do pedido |

#### 🔗 ItemPedido
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `pedido` | `ForeignKey` → `Pedido` | Pedido associado (CASCADE) |
| `brinquedo` | `ForeignKey` → `Brinquedo` | Brinquedo alugado (PROTECT) |
| `preco_no_momento` | `DecimalField` (8,2) | Preço do brinquedo no momento do pedido (congelado) |

---

## 🌐 Endpoints da API

> **Base URL:** `http://localhost:8000/api/v1/`

### Categorias

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/v1/categorias/` | Lista todas as categorias |
| `POST` | `/api/v1/categorias/` | Cria uma nova categoria |
| `GET` | `/api/v1/categorias/{id}/` | Detalhes de uma categoria |
| `PUT` | `/api/v1/categorias/{id}/` | Atualiza uma categoria |
| `PATCH` | `/api/v1/categorias/{id}/` | Atualização parcial de uma categoria |
| `DELETE` | `/api/v1/categorias/{id}/` | Remove uma categoria |

### Brinquedos

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/v1/brinquedos/` | Lista todos os brinquedos |
| `POST` | `/api/v1/brinquedos/` | Cria um novo brinquedo |
| `GET` | `/api/v1/brinquedos/{id}/` | Detalhes de um brinquedo |
| `PUT` | `/api/v1/brinquedos/{id}/` | Atualiza um brinquedo |
| `PATCH` | `/api/v1/brinquedos/{id}/` | Atualização parcial de um brinquedo |
| `DELETE` | `/api/v1/brinquedos/{id}/` | Remove um brinquedo |

**Parâmetros de filtro e busca:**
| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `?categoria={id}` | Filtro por categoria | `?categoria=1` |
| `?status_atual={status}` | Filtro por status | `?status_atual=disponivel` |
| `?search={termo}` | Busca textual (nome, descrição, código) | `?search=Lego` |

### Pedidos

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/v1/pedidos/` | Lista todos os pedidos |
| `POST` | `/api/v1/pedidos/` | Cria um novo pedido |
| `GET` | `/api/v1/pedidos/{id}/` | Detalhes de um pedido |
| `PUT` | `/api/v1/pedidos/{id}/` | Atualiza um pedido |
| `PATCH` | `/api/v1/pedidos/{id}/` | Atualização parcial de um pedido |
| `DELETE` | `/api/v1/pedidos/{id}/` | Remove um pedido |

### Clientes

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/v1/clientes/` | Lista todos os clientes |
| `POST` | `/api/v1/clientes/` | Cria um novo cliente (já cria o User do Django) |
| `GET` | `/api/v1/clientes/{id}/` | Detalhes de um cliente |
| `PUT` | `/api/v1/clientes/{id}/` | Atualiza um cliente |
| `PATCH` | `/api/v1/clientes/{id}/` | Atualização parcial de um cliente |
| `DELETE` | `/api/v1/clientes/{id}/` | Remove um cliente |

### Autenticação JWT

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/v1/token/` | Gera tokens de acesso e refresh |
| `POST` | `/api/v1/token/refresh/` | Renova o token de acesso |

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.x instalado
- Git (opcional)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/caixa-magica-api.git
cd caixa-magica-api

# 2. Crie o ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute as migrações
python manage.py migrate

# 6. Inicie o servidor de desenvolvimento
python manage.py runserver
```

O servidor estará disponível em **http://localhost:8000/**.

> 💡 Você também pode acessar a interface web do Django REST Framework diretamente pelo navegador para testar os endpoints de forma interativa em `http://localhost:8000/api/v1/`.

---

## 📝 Exemplos de Uso

### 1. Criar um cliente

```bash
POST /api/v1/clientes/
```

```json
{
    "username": "joaosilva",
    "email": "joao@email.com",
    "password": "senha123",
    "first_name": "João",
    "telefone": "11988887777",
    "endereco_padrao": "Rua das Flores, 123 - Centro, São Paulo - SP"
}
```

**Resposta (201 Created):**
```json
{
    "id": 1,
    "user": 1,
    "telefone": "11988887777",
    "endereco_padrao": "Rua das Flores, 123 - Centro, São Paulo - SP"
}
```

### 2. Obter token JWT

```bash
POST /api/v1/token/
```

```json
{
    "username": "joaosilva",
    "password": "senha123"
}
```

**Resposta (200 OK):**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIs...",
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

### 3. Listar brinquedos com filtros e busca

```bash
# Listar todos os brinquedos disponíveis
GET /api/v1/brinquedos/?status_atual=disponivel

# Buscar brinquedos por nome ou código
GET /api/v1/brinquedos/?search=Lego

# Combinar filtros
GET /api/v1/brinquedos/?categoria=1&status_atual=disponivel&search=carrinho
```

**Resposta (200 OK):**
```json
[
    {
        "id": 1,
        "nome": "Lego Classic",
        "descricao_curta": "Kit de blocos de montar",
        "descricao_completa": "Kit com 500 peças para montar...",
        "codigo": "LEGO-001",
        "categoria": {
            "id": 1,
            "nome": "Montar",
            "descricao": "Brinquedos de montar"
        },
        "categoria_id": 1,
        "valor_base": "29.90",
        "regras_aluguel": "Devolver limpo e completo.",
        "status_atual": "disponivel",
        "idade_recomendada": "4+",
        "imagens": [
            {
                "id": 1,
                "imagem_url": "https://exemplo.com/lego-capa.jpg",
                "ordem": 0
            }
        ]
    }
]
```

### 4. Criar um pedido

```bash
POST /api/v1/pedidos/
Authorization: Bearer <seu-token-jwt>
```

```json
{
    "cliente": 1,
    "prazo_aluguel": 7,
    "tipo_logistica": "entrega",
    "endereco_entrega": "Rua das Flores, 123 - Centro, São Paulo - SP",
    "valor_total": 59.90
}
```

**Resposta (201 Created):**
```json
{
    "id": 1,
    "cliente": 1,
    "prazo_aluguel": 7,
    "tipo_logistica": "entrega",
    "endereco_entrega": "Rua das Flores, 123 - Centro, São Paulo - SP",
    "status_aluguel": "pendente",
    "valor_total": "59.90",
    "data_criacao": "2026-01-15T14:30:00Z"
}
```

---

## 📁 Estrutura do Projeto

```
caixa-magica-api/
├── catalogo/                        # App principal do catálogo
│   ├── migrations/                  # Migrações do banco de dados
│   │   ├── 0001_initial.py          # Migração inicial
│   │   └── 0002_remove_...py        # Migração de ajuste (imagens)
│   ├── __init__.py
│   ├── admin.py                     # Configuração do Django Admin
│   ├── apps.py                      # Configuração do app
│   ├── models.py                    # Modelos de dados
│   ├── serializers.py               # Serializadores (conversão JSON)
│   ├── tests.py                     # Testes automatizados
│   └── views.py                     # Views (controladores da API)
├── setup/                           # Configuração do projeto Django
│   ├── __init__.py
│   ├── asgi.py                      # Configuração ASGI
│   ├── settings.py                  # Configurações do projeto
│   ├── urls.py                      # Rotas principais
│   └── wsgi.py                      # Configuração WSGI
├── .gitignore
├── db.sqlite3                       # Banco de dados SQLite
├── manage.py                        # Gerenciador Django CLI
├── README.md                        # Este arquivo
└── requirements.txt                 # Dependências do projeto
```

---

## 🔧 Desenvolvimento

### Como contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Testes

```bash
python manage.py test
```

### Criar superusuário (para acessar o admin)

```bash
python manage.py createsuperuser
```

Acesse o painel admin em: `http://localhost:8000/admin/`

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">
  <p>Desenvolvido como parte do projeto final do CEPEDI 🎓</p>
  <p>
    <a href="#-caixa-mágica---api">Voltar ao topo ↑</a>
  </p>
</div>

