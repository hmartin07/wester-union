from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TransaccionViewSet, CuentaBancariaViewSet
from .views import TarifaViewSet

# 🔹 Configurar Router para las vistas de Transacciones y Cuentas
router = DefaultRouter()
router.register(r'transacciones', TransaccionViewSet, basename="transaccion")
router.register(r'cuentas', CuentaBancariaViewSet, basename="cuenta_bancaria")
router.register(r'tarifas', TarifaViewSet, basename="tarifa")

urlpatterns = [
    path('api/', include(router.urls)),  # 🔹 Prefijo API para organizar mejor
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
