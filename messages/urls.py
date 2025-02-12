from django.urls import path
from .views import enviar_factura

urlpatterns = [
    path('enviar-factura/', enviar_factura, name='enviar_factura'),
]
