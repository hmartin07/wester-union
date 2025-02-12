from django.db import models
from django.contrib.auth.models import User

# Modelo de Transacción
class Transaccion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido')
    ]

    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transacciones")
    destinatario_nombre = models.CharField(max_length=255)
    destinatario_pais = models.CharField(max_length=100)
    destinatario_telefono = models.CharField(max_length=20, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.remitente.username} -> {self.destinatario_nombre} ({self.estado})"

# Modelo de Notificaciones
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notificaciones")
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f"Notificación para {self.usuario.username}"
