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

]

# Configuración de la base de datos MySQL en Docker
# Configuración de la base de datos MySQL en Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'envio_dinero',
        'USER': 'root',
        'PASSWORD': '12deoctubre',
        'HOST': 'localhost',
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
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Configuración de Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Tu frontend en Vite
]

CORS_ALLOW_CREDENTIALS = True  # Para permitir cookies y autenticación en las peticiones


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

AUTH_USER_MODEL = 'usuarios.Usuario'


SECRET_KEY = 'jwt%qp2uo=872d#fx8ykal@*(@ixwsik50@w(ezp776stra62&'

# Configuración de CORS para permitir el acceso al frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Cambia esto según la URL de tu frontend
]


ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']  # Agrega los hosts que necesites

DEBUG = True


STATIC_URL = '/static/'


ROOT_URLCONF = 'backend.urls'
