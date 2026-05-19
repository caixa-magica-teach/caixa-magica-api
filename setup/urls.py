from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import CategoriaViewSet, BrinquedoViewSet

# O Router cria automaticamente rotas para listagem e detalhes
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'brinquedos', BrinquedoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Todas as rotas geradas ficarão sob /api/v1/
    path('api/v1/', include(router.urls))
]
