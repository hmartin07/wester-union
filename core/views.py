from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Transaccion, CuentaBancaria, Tarifa
from .serializers import TransaccionSerializer, CuentaBancariaSerializer, TarifaSerializer


class CuentaBancariaViewSet(viewsets.ModelViewSet):
    serializer_class = CuentaBancariaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Mostrar solo cuentas del usuario autenticado"""
        if self.request.user.is_authenticated:
            return CuentaBancaria.objects.filter(usuario=self.request.user)
        return CuentaBancaria.objects.none()  # Retorna un QuerySet vacío si no está autenticado


class TransaccionViewSet(viewsets.ModelViewSet):
    serializer_class = TransaccionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Mostrar solo transacciones del usuario autenticado"""
        return Transaccion.objects.filter(remitente=self.request.user)

    def create(self, request, *args, **kwargs):
        """Validar existencia de las cuentas bancarias antes de crear la transacción"""
        
        if isinstance(request.data, list):  # Si el request es una lista de transacciones
            transacciones_validas = []
            errores = []

            for item in request.data:
                item['remitente'] = request.user.id  # Asigna el remitente autenticado
                
                # Verificar si cuenta_remitente existe
                cuenta_remitente_id = item.get('cuenta_remitente')
                if cuenta_remitente_id and not CuentaBancaria.objects.filter(id=cuenta_remitente_id).exists():
                    errores.append({"cuenta_remitente": f"La cuenta remitente {cuenta_remitente_id} no existe."})
                    continue  # Salta a la siguiente transacción
                
                # Verificar si cuenta_destinatario existe
                cuenta_destinatario_id = item.get('cuenta_destinatario')
                if cuenta_destinatario_id and not CuentaBancaria.objects.filter(id=cuenta_destinatario_id).exists():
                    errores.append({"cuenta_destinatario": f"La cuenta destinataria {cuenta_destinatario_id} no existe."})
                    continue  # Salta a la siguiente transacción
                
                transacciones_validas.append(item)

            if not transacciones_validas:
                return Response({"error": "No se pudo crear ninguna transacción.", "detalles": errores}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=transacciones_validas, many=True)
        
        else:  # Si es un solo objeto
            data = request.data.copy()
            data['remitente'] = request.user.id  # Asigna el remitente autenticado

            # Verificar si cuenta_remitente existe
            cuenta_remitente_id = data.get('cuenta_remitente')
            if cuenta_remitente_id and not CuentaBancaria.objects.filter(id=cuenta_remitente_id).exists():
                return Response({"cuenta_remitente": f"La cuenta remitente {cuenta_remitente_id} no existe."}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar si cuenta_destinatario existe
            cuenta_destinatario_id = data.get('cuenta_destinatario')
            if cuenta_destinatario_id and not CuentaBancaria.objects.filter(id=cuenta_destinatario_id).exists():
                return Response({"cuenta_destinatario": f"La cuenta destinataria {cuenta_destinatario_id} no existe."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TarifaViewSet(viewsets.ModelViewSet):
    queryset = Tarifa.objects.all()
    serializer_class = TarifaSerializer
    pagination_class = None 
