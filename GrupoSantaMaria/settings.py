import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- ALLAUTH CONFIGURATIONS ---
SITE_ID = 1

# Método de autenticación: Permite iniciar sesión con nombre de usuario o email
# Esto es crucial para permitir ambos.
ACCOUNT_AUTHENTICATION_METHOD = 'username_email' # Reemplaza el deprecado ACCOUNT_LOGIN_METHODS

# Requerir email en el registro
ACCOUNT_EMAIL_REQUIRED = True

# No requerir nombre de usuario si solo quieres usar email (pero si quieres ambos, cámbialo a True)
# Dado que mencionas "usuario y contraseña", lo dejaremos como True para permitir nombres de usuario.
ACCOUNT_USERNAME_REQUIRED = True # Cambiado a True para permitir registro con username

# Pedir confirmación de contraseña en el registro
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True

# Asegurar que el email sea único para cada cuenta
ACCOUNT_UNIQUE_EMAIL = True

# Donde redirigir después del login exitoso
LOGIN_REDIRECT_URL = '/'

# Donde redirigir después del logout
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'

# Permite la funcionalidad "recordarme" en el login
ACCOUNT_SESSION_REMEMBER = True

# Configuraciones de Social Account (específicas para Google)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # Para la versión 4.1.6 de Django y Allauth más recientes,
        # 'APP' ya no se usa directamente aquí, sino que se configuran
        # las credenciales en el Admin de Django (Sitios -> Social applications).
        # Sin embargo, si tu versión de Allauth es más antigua o si prefieres
        # mantener las credenciales aquí por simplicidad temporal, lo dejaremos.
        # Pero la forma recomendada es configurarlo en el admin.
        'APP': {
            'client_id': 'YOUR_GOOGLE_CLIENT_ID', # <-- ¡IMPORTANTE! Reemplaza con tu ID de cliente de Google
            'secret': 'YOUR_GOOGLE_SECRET',       # <-- ¡IMPORTANTE! Reemplaza con tu secreto de cliente de Google
            'key': '' # La clave generalmente no se usa para Google
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
# --- FIN ALLAUTH CONFIGURATIONS ---


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)6pltvtx)dwa5r56v(-esu+s6ondf7n855t6ei@3bh&0y+jndj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Aplicaciones.Principal',
    'Aplicaciones.Modulo1',
    'Aplicaciones.Modulo2',
    'Aplicaciones.Modulo3',
    'Aplicaciones.Vehiculos', # Confirmado que es 'Aplicaciones.Vehiculos'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 
]

ROOT_URLCONF = 'GrupoSantaMaria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Asegúrate de tener una carpeta 'templates' en la raíz de tu proyecto
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # allauth requiere esto
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'GrupoSantaMaria.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'GrupoSantaMaria',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
STATIC_URL = '/static/'

# ¡CAMBIO AQUÍ! Ahora apuntas DENTRO de la carpeta del proyecto
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'GrupoSantaMaria', 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Este está bien fuera

MEDIA_URL = '/media/'
# ¡CAMBIO AQUÍ! También apuntas DENTRO de la carpeta del proyecto para 'media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'GrupoSantaMaria', 'media')


# --- Configuración adicional para Allauth ---
# Backend de autenticación
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Requerido para iniciar sesión con nombre de usuario/contraseña
    'allauth.account.auth_backends.AuthenticationBackend', # Requerido para iniciar sesión con Allauth (email, social)
]

