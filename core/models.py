from django.db import models
from django.conf import settings  # Usamos AUTH_USER_MODEL para referenciar usuarios
import uuid
from django.utils import timezone

# Modelo de Cuenta Bancaria
class CuentaBancaria(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cuentas")
    banco = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=50, unique=True)
    tipo_cuenta = models.CharField(max_length=20, choices=[("Ahorros", "Ahorros"), ("Corriente", "Corriente")])
    moneda = models.CharField(max_length=10, default="USD")

    def __str__(self):
        return f"{self.banco} - {self.numero_cuenta} ({self.usuario.username})"

# Modelo de Transacción Mejorada
class Transaccion(models.Model):
    METODOS_PAGO = [
        ("Transferencia Bancaria", "Transferencia Bancaria"),
        ("Tarjeta de Crédito", "Tarjeta de Crédito"),
        ("PayPal", "PayPal"),
        ("Efectivo", "Efectivo"),
    ]

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("aprobada", "Aprobada"),
        ("rechazada", "Rechazada"),
        ("completada", "Completada"),
    ]

    id_transaccion = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    remitente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="transacciones_enviadas"
    )
    cuenta_remitente = models.ForeignKey(
        CuentaBancaria, 
        on_delete=models.PROTECT,  # Evita eliminar cuentas usadas en transacciones
        null=True, blank=True, 
        related_name="transacciones_envio"
    )
    destinatario_nombre = models.CharField(max_length=255)
    destinatario_pais = models.CharField(max_length=100)
    destinatario_telefono = models.CharField(max_length=20, blank=True, null=True)
    cuenta_destinatario = models.ForeignKey(
        CuentaBancaria, 
        on_delete=models.PROTECT,  # Evita que una cuenta eliminada deje transacciones sin referencia
        null=True, blank=True, 
        related_name="transacciones_recepcion"
    )
    moneda = models.CharField(max_length=10, default="USD")
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    comision = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    metodo_pago = models.CharField(max_length=30, choices=METODOS_PAGO)
    
    numero_referencia = models.CharField(
        max_length=100, 
        unique=True, 
        blank=True, null=True, 
        default=uuid.uuid4  # Evita problemas con valores NULL en campo único
    )

    estado = models.CharField(max_length=15, choices=ESTADOS, default="pendiente")
    fecha_creacion = models.DateTimeField(default=timezone.now)  # Permite actualizar fecha manualmente
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        remitente = self.remitente.username if self.remitente else "Desconocido"
        return f"Transacción {self.id_transaccion} - {remitente} → {self.destinatario_nombre} ({self.estado})"
class Tarifa(models.Model):
    pais = models.CharField(max_length=100, unique=True)
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.pais}: {self.comision}$ - {self.impuesto}%"
    
    #commit