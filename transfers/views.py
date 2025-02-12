from rest_framework import viewsets
from .models import Country, Transfer
from .serializers import CountrySerializer, TransferSerializer
from rest_framework.permissions import IsAuthenticated

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
