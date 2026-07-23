from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalogo.views import CategoriaViewSet, BrinquedoViewSet, PedidoViewSet, ClienteViewSet

# 1. ADICIONEI ESSA LINHA PARA TRAZER AS TELAS DE LOGIN/TOKEN
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# O Router cria automaticamente rotas para listagem e detalhes
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'brinquedos', BrinquedoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'clientes', ClienteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Todas as rotas geradas ficarão sob /api/v1/
    # E utilizamos Versionamento de API (v1) para facilitar futuras mudanças
    path('api/v1/', include(router.urls)),

    # 2. ADICIONAMOS ESSAS DUAS LINHAS PARA CRIAR AS ROTAS DE TOKEN (LOGIN)
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

