# urls.py global
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transfers.views import TransferViewSet, CountryViewSet

router = DefaultRouter()
router.register(r'transfers', TransferViewSet)
router.register(r'countries', CountryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/users/', include('users.urls')),
    path('api/', include(router.urls)),  # Aquí se incluyen las rutas del router
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]
