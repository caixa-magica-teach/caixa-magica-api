from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 1. IMPORTE A VIEWSET DAS IMAGENS AQUI (ex: ImagemBrinquedoViewSet)
from catalogo.views import (
    CategoriaViewSet, 
    BrinquedoViewSet, 
    PedidoViewSet, 
    ClienteViewSet,
    ImagemBrinquedoViewSet  # <--- ADICIONE AQUI
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'brinquedos', BrinquedoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'clientes', ClienteViewSet)

# 2. REGISTRE A ROTA DAS IMAGENS NO ROUTER
router.register(r'imagens', ImagemBrinquedoViewSet)  # <--- ADICIONE ESTA LINHA

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]