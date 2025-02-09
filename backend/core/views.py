from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Transaccion, Notificacion
from .serializers import TransaccionSerializer, NotificacionSerializer

class TransaccionViewSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer
    permission_classes = [IsAuthenticated]

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]
