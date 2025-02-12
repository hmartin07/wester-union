import os
from pathlib import Path
from dotenv import load_dotenv

# 🔹 Definir BASE_DIR al inicio
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔹 Cargar variables de entorno desde .env
load_dotenv()

# 🔹 Configuración de archivos estáticos (ahora BASE_DIR está definido antes de usarse)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# 🔹 Seguridad: SECRET_KEY ahora se obtiene desde el .env
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'clave_por_defecto_cambiar')

# 🔹 Permitir cambiar DEBUG desde el .env
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1')

# 🔹 Hosts permitidos
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# 🔹 URL principal
ROOT_URLCONF = 'backend.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework_simplejwt',

    # Apps del Proyecto
    'core',

    # Django REST Framework
    'rest_framework',
]

# 🔹 Configuración de la base de datos MySQL en Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'envio_dinero'),
        'USER': os.getenv('DB_USER', 'usuario_mysql'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'Clases.2024'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3308'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# 🔹 Configuración de DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# 🔹 Configuración de Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🔹 Configuración de Templates
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
