import random
from django.core.mail import send_mail
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, LoginSerializer

class RegisterView(views.APIView):
    def post(self, request):
        # Serializador para crear un usuario
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Crear usuario y generar código de verificación
            user = serializer.save()
            verification_code = str(random.randint(1000, 9999))
            user.verification_code = verification_code
            user.save()

            # Enviar el código de verificación por correo
            send_mail(
                'Código de verificación',
                f'Tu código de verificación es {verification_code}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Te hemos enviado un código de verificación al correo."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(views.APIView):
    def post(self, request):
        # Obtener email y código de la solicitud
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            user = User.objects.get(email=email)
            if user.verification_code == code:
                user.is_verified = True
                user.save()
                return Response({"message": "Cuenta verificada correctamente."}, status=status.HTTP_200_OK)
            return Response({"message": "Código incorrecto."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

class LoginView(views.APIView):
    def post(self, request):
        # Serializador para login
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user and user.is_verified:
                # Crear el token de acceso y refresh con JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }, status=status.HTTP_200_OK)
            return Response({"message": "Credenciales incorrectas o cuenta no verificada."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(views.APIView):
    def post(self, request):
        # Obtener el email del usuario que necesita el reset de contraseña
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            reset_code = str(random.randint(1000, 9999))
            user.verification_code = reset_code
            user.save()

            # Enviar el código de recuperación al correo del usuario
            send_mail(
                'Código para restablecer la contraseña',
                f'Tu código de restablecimiento es {reset_code}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Te hemos enviado un código de restablecimiento."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Correo no registrado."}, status=status.HTTP_404_NOT_FOUND)
