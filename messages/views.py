from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import enviar_correo_factura

@csrf_exempt
def enviar_factura(request):
    """Vista para enviar una factura por correo."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Intenta leer los datos como JSON
            email_cliente = data.get("email")
            datos_factura = {
                "cliente": data.get("cliente", "Cliente Desconocido"),
                "total": data.get("total", "0.00"),
                "direccion": data.get("direccion", "Dirección desconocida"),  # Asegúrate de que "direccion" esté presente
                "email": email_cliente,
                "items": data.get("items", []),
            }

            if email_cliente:
                enviar_correo_factura(email_cliente, datos_factura)
                return JsonResponse({"mensaje": "Factura enviada correctamente."})
            else:
                return JsonResponse({"error": "Email del cliente no proporcionado."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de datos incorrecto."}, status=400)

    return JsonResponse({"error": "Método no permitido."}, status=405)
