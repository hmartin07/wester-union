from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'users',
    'django_rest_passwordreset',
    # Apps del Proyecto
    'core',
    'api',
    'djoser',
    'transfers',
]

# Configuración para enviar correos electrónicos
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Usando Gmail como ejemplo
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'soportealex68@gmail.com'  # Tu correo de envío
EMAIL_HOST_PASSWORD = 'bpqy goan yadw qjtd'  # La contraseña de tu correo

# Configuración de la base de datos MySQL en Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'envio_dinero',
        'USER': 'root',
        'PASSWORD': '12deoctubre',
        'HOST': 'localhost',  # Si estás usando Docker, asegúrate de que el contenedor de MySQL esté corriendo
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# Configuración de DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Default permission, can be overridden
    ),
}


SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'reset-password/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SEND_CONFIRMATION_EMAIL': False,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuración de Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Agregar en la parte superior
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de CORS para permitir acceso desde el frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Tu frontend en Vite
    "http://localhost:3000",  # Otro puerto para frontend si lo necesitas
]

CORS_ALLOW_CREDENTIALS = True  # Para permitir cookies y autenticación en las peticiones
CORS_ALLOW_ALL_ORIGINS = True  # Permitir cualquier origen (aunque puedes ajustarlo a tus necesidades)

# Configuración de Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración para el modelo de usuario personalizado
AUTH_USER_MODEL = 'users.User'

# Clave secreta para Django (asegúrate de cambiarla en producción)
SECRET_KEY = 'jwt%qp2uo=872d#fx8ykal@*(@ixwsik50@w(ezp776stra62&'

# Configuración de CORS para permitir el acceso al frontend
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']  # Agrega los hosts que necesites

DEBUG = True  # Cambia esto a False en producción

STATIC_URL = '/static/'

ROOT_URLCONF = 'backend.urls'
