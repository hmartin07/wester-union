from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TransaccionViewSet, NotificacionViewSet
from .views import DescargarComprobante
from .views import EnviarCorreoNotificacion

# 🔹 Registrar las vistas en el router
router = DefaultRouter()
router.register(r'transacciones', TransaccionViewSet, basename="transaccion")
router.register(r'notificaciones', NotificacionViewSet, basename="notificacion")

# 🔹 Incluir todas las rutas en urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # 🔹 Asegura que el router esté incluido
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('transaccion/<int:pk>/comprobante/', DescargarComprobante.as_view({'get': 'retrieve'})),
    path('transaccion/<int:pk>/notificar/', EnviarCorreoNotificacion.as_view({'post': 'create'})),
]

