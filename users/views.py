import random
from django.core.mail import send_mail
from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import User
from .serializers import UserSerializer, LoginSerializer

User = get_user_model()

# Vista para registrar un usuario
class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_verified=False, is_active=False)
            verification_code = str(random.randint(1000, 9999))
            user.verification_code = verification_code
            user.save()

            send_mail(
                'Código de verificación',
                f'Tu código de verificación es {verification_code}',
                'soportealex68@gmail.com',
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "Te hemos enviado un código de verificación al correo."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para verificar el código
class VerifyCodeView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = User.objects.get(email=email)

            if user.verification_code == code:
                user.is_verified = True
                user.is_active = True
                user.save()
                return Response({"message": "Cuenta verificada correctamente."}, status=status.HTTP_200_OK)
            
            return Response({"message": "Código incorrecto."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"message": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)


# Vista para iniciar sesión
class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print("Datos recibidos:", request.data)  # Debug
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
                print(f"Usuario encontrado: {user.email}")  # Debug
            except User.DoesNotExist:
                return Response({"message": "Correo o contraseña incorrectos."}, status=status.HTTP_400_BAD_REQUEST)

            if not user.check_password(password):
                return Response({"message": "Correo o contraseña incorrectos."}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_verified or not user.is_active:
                return Response({"message": "Cuenta no verificada o desactivada."}, status=status.HTTP_400_BAD_REQUEST)

            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para restablecer la contraseña
class PasswordResetView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
            reset_code = str(random.randint(1000, 9999))

            user.verification_code = reset_code
            user.save()

            send_mail(
                'Código para restablecer la contraseña',
                f'Tu código de restablecimiento es {reset_code}',
                'soportealex68@gmail.com',
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "Te hemos enviado un código de restablecimiento."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "Correo no registrado."}, status=status.HTTP_404_NOT_FOUND)
