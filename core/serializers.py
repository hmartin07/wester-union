from rest_framework import serializers
from .models import Transaccion, CuentaBancaria
from .models import Tarifa
class CuentaBancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaBancaria
        fields = '__all__'

class TransaccionSerializer(serializers.ModelSerializer):
    cuenta_remitente = serializers.PrimaryKeyRelatedField(
        queryset=CuentaBancaria.objects.all(), required=False
    )
    cuenta_destinatario = serializers.PrimaryKeyRelatedField(
        queryset=CuentaBancaria.objects.all(), required=False
    )

    class Meta:
        model = Transaccion
        fields = '__all__'

    def validate(self, data):
        """ Validar valores numéricos y calcular comisiones/impuestos """
        errores = {}

        if 'monto' in data and data['monto'] <= 0:
            errores['monto'] = "El monto debe ser mayor a 0."

        # Buscar tarifa del país del destinatario
        tarifa = Tarifa.objects.filter(pais=data.get('destinatario_pais')).first()
        if tarifa:
            data['comision'] = (data['monto'] * tarifa.comision) / 100
            data['impuesto'] = (data['monto'] * tarifa.impuesto) / 100
        else:
            errores['destinatario_pais'] = "No hay tarifa configurada para este país."

        if errores:
            raise serializers.ValidationError(errores)

        return data
class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
        fields = '__all__'

    def validate_pais(self, value):
        """ Evitar tarifas duplicadas por país """
        if Tarifa.objects.filter(pais=value).exists():
            raise serializers.ValidationError("Ya existe una tarifa para este país.")
        return value
    #commit