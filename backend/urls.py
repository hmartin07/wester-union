from django.contrib import admin
from django.urls import path, include
from messages.views import enviar_factura
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/users/', include('users.urls')),
    path('messages/enviar-factura/', enviar_factura, name='enviar_factura'),
]
