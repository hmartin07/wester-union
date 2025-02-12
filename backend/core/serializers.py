from rest_framework import serializers
from .models import Transaccion, Notificacion

class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'

    def validate_monto(self, value):
        """ Validar que el monto sea positivo """
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a 0.")
        return value

    def validate_comision(self, value):
        """ Validar que la comisión no sea negativa """
        if value < 0:
            raise serializers.ValidationError("La comisión no puede ser negativa.")
        return value

    def validate_impuesto(self, value):
        """ Validar que el impuesto no sea negativo """
        if value < 0:
            raise serializers.ValidationError("El impuesto no puede ser negativo.")
        return value


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'
