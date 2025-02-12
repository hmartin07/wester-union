# urls.py global
from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from messages.views import enviar_factura
=======
from rest_framework.routers import DefaultRouter
from transfers.views import TransferViewSet, CountryViewSet

router = DefaultRouter()
router.register(r'transfers', TransferViewSet)
router.register(r'countries', CountryViewSet)

>>>>>>> b9e91aa2d357f726b29511b80dcf7a020cbeea27
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/users/', include('users.urls')),
<<<<<<< HEAD
    path('messages/enviar-factura/', enviar_factura, name='enviar_factura'),
=======
    path('api/', include(router.urls)),  # Aquí se incluyen las rutas del router
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
>>>>>>> b9e91aa2d357f726b29511b80dcf7a020cbeea27
]
