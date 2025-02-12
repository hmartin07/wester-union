from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Transaccion, Notificacion
from .serializers import TransaccionSerializer, NotificacionSerializer
import io
from django.http import FileResponse, Http404
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.http import JsonResponse


class TransaccionViewSet(viewsets.ModelViewSet):
    serializer_class = TransaccionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Mostrar solo transacciones del usuario autenticado """
        return Transaccion.objects.filter(remitente=self.request.user)

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Mostrar solo notificaciones del usuario autenticado """
        return Notificacion.objects.filter(usuario=self.request.user)
def generar_pdf(transaccion):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    # Agregar detalles al PDF
    p.drawString(100, 800, f"Comprobante de Transacción")
    p.drawString(100, 780, f"ID Transacción: {transaccion.id}")
    p.drawString(100, 760, f"Remitente: {transaccion.remitente.username}")
    p.drawString(100, 740, f"Destinatario: {transaccion.destinatario_nombre}")
    p.drawString(100, 720, f"Monto: {transaccion.monto} USD")
    p.drawString(100, 700, f"Comisión: {transaccion.comision} USD")
    p.drawString(100, 680, f"Impuesto: {transaccion.impuesto} USD")
    p.drawString(100, 660, f"Estado: {transaccion.estado}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

class DescargarComprobante(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        transaccion = get_object_or_404(Transaccion, id=pk)
        pdf_buffer = generar_pdf(transaccion)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f"comprobante_{transaccion.id}.pdf")
    
class EnviarCorreoNotificacion(viewsets.ViewSet):
    def create(self, request, pk=None):
        transaccion = get_object_or_404(Transaccion, id=pk)
        
        asunto = "Confirmación de Envío de Dinero"
        mensaje = f"""
        Estimado {transaccion.remitente.username},

        Su transacción ha sido procesada con éxito.
        
        Detalles:
        - Monto: {transaccion.monto} USD
        - Comisión: {transaccion.comision} USD
        - Impuesto: {transaccion.impuesto} USD
        - Estado: {transaccion.estado}
        
        Gracias por usar nuestro servicio.
        """
        destinatario = transaccion.remitente.email

        try:
            send_mail(asunto, mensaje, 'no-reply@sistema.com', [destinatario])
            return JsonResponse({"mensaje": "Correo enviado correctamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)