from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransaccionViewSet, NotificacionViewSet

router = DefaultRouter()
router.register(r'transacciones', TransaccionViewSet)
router.register(r'notificaciones', NotificacionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
